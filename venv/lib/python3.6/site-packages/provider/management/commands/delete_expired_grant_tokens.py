"""
Command to delete expired OAuth2 grant tokens from the oauth2_grant table.
"""

import logging

from provider.oauth2.models import Grant
from ._delete_common import DeleteCommand

log = logging.getLogger(__name__)


class Command(DeleteCommand):
    """
    Example usage: ./manage.py lms --settings=devstack delete_expired_grant_tokens.py
    """
    help = 'Deletes all expired OAuth2 grant tokens (in chunks).'
    model = Grant

    def handle(self, *args, **options):
        """
        Deletes expired oauth2_grant tokens, chunking the deletes to avoid long table/row locks.
        """
        self._handle(*args, **options)
