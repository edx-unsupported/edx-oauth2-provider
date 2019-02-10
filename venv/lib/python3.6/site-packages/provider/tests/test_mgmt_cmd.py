"""
Unittests for testing management commands.
"""
import logging
import unittest
import uuid
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError

from provider import constants
from provider.management.commands.delete_expired_grant_tokens import Command
from provider.oauth2.models import Client, Grant, AccessToken, RefreshToken

log = logging.getLogger(__name__)


class _TokenDeletionTestCase(unittest.TestCase):
    """
    Tests for the `delete_expired_grant_tokens` management command.
    """
    model = None
    command_name = None

    def setUp(self):
        super(_TokenDeletionTestCase, self).setUp()
        self.command = Command()

        # Make User and Client.
        user = User.objects.create_user(uuid.uuid4().hex, '%s@example.com' % uuid.uuid4().hex)
        client = Client.objects.create(client_type=constants.CONFIDENTIAL)
        # Make some expired grant tokens.
        expire_time = datetime.now() - timedelta(4)
        log.info("Creating 10 tokens expiring on %s.", expire_time)
        for i in range(10):
            # Make sure AccessTokens have their associated RefreshTokens.
            if self.model == AccessToken:
                x = AccessToken.objects.create(expires=expire_time, client_id=client.id, user_id=user.id)
                RefreshToken.objects.create(client_id=client.id, user_id=user.id, access_token=x, expired=True)
            else:
                self.model.objects.create(expires=expire_time, client_id=client.id, user_id=user.id)

        # Make User and Client.
        user = User.objects.create_user(uuid.uuid4().hex, '%s@example.com' % uuid.uuid4().hex)
        client = Client.objects.create(client_type=constants.CONFIDENTIAL)
        # Make some non-expired grant tokens.
        expire_time = datetime.now() + timedelta(4)
        log.info("Creating 10 tokens expiring on %s.", expire_time)
        for i in range(10):
            if self.model == AccessToken:
                x = AccessToken.objects.create(expires=expire_time, client_id=client.id, user_id=user.id)
                RefreshToken.objects.create(client_id=client.id, user_id=user.id, access_token=x, expired=False)
            else:
                self.model.objects.create(expires=expire_time, client_id=client.id, user_id=user.id)

    def tearDown(self):
        super(_TokenDeletionTestCase, self).tearDown()
        # Remove ALL tokens.
        self.model.objects.all().delete()

        if self.model == AccessToken:
            RefreshToken.objects.all().delete()

    def test_negative_chunk_arg(self):
        errstring = "Only positive chunk size is allowed"
        with self.assertRaisesRegexp(CommandError, errstring):
            self.command.handle(self.command_name, chunk_size=-1000)

    def test_zero_chunk_arg(self):
        errstring = "Only positive chunk size is allowed"
        with self.assertRaisesRegexp(CommandError, errstring):
            self.command.handle(self.command_name, chunk_size=0)

    def test_negative_sleep_arg(self):
        errstring = "Only non-negative sleep between seconds is allowed"
        with self.assertRaisesRegexp(CommandError, errstring):
            self.command.handle(self.command_name, sleep_between=-5.5)

    def test_single_chunk_delete(self):
        call_command(self.command_name)
        self.assertEqual(self.model.objects.all().count(), 10)

    def test_multiple_chunk_delete(self):
        call_command(self.command_name, chunk_size=2)
        self.assertEqual(self.model.objects.all().count(), 10)

    def test_nothing_to_delete(self):
        call_command(self.command_name)
        self.assertEqual(self.model.objects.all().count(), 10)
        # call it again, there's nothing left to delete and it
        # should handle that case.
        call_command(self.command_name)
        self.assertEqual(self.model.objects.all().count(), 10)

class TestDeleteExpiredGrantTokens(_TokenDeletionTestCase):
    """
    Tests for the `delete_expired_grant_tokens` management command.
    """
    model = Grant
    command_name = "delete_expired_grant_tokens"


class TestDeleteExpiredAccessTokens(_TokenDeletionTestCase):
    """
    Tests for the `delete_expired_access_tokens` management command.
    """
    model = AccessToken
    command_name = "delete_expired_access_tokens"

    def test_refresh_token_deletes_with_access_token(self):
        call_command(self.command_name, chunk_size=2)
        self.assertEqual(self.model.objects.all().count(), 10)
        self.assertEqual(RefreshToken.objects.all().count(), 10)
