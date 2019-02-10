"""
Command to delete expired OAuth2 access tokens from the oauth2_accesstoken table.
"""

import logging

from provider.oauth2.models import AccessToken
from ._delete_common import DeleteCommand

log = logging.getLogger(__name__)


class Command(DeleteCommand):
    """
    Example usage: ./manage.py lms --settings=devstack delete_expired_access_tokens.py
    """
    help = 'Deletes all expired OAuth2 access tokens (in chunks).'
    model = AccessToken

    def handle(self, *args, **options):
        """
        Deletes expired oauth2_accesstoken tokens, chunking the deletes to avoid long table/row locks.
        """
        self._handle(*args, **options)
