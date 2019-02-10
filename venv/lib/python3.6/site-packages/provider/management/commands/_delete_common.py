"""
Base Command class to delete expired rows from the various oauth2 tables.
"""

from django.utils import timezone
import logging
import time
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Min, Max

log = logging.getLogger(__name__)


class DeleteCommand(BaseCommand):
    """
    Base class for things that delete in batches.
    """

    # Default maximum number of expired tokens to delete in a single transaction.
    DEFAULT_CHUNK_SIZE = 10000

    # Default seconds to sleep between chunked deletes of expired tokens.
    DEFAULT_SLEEP_BETWEEN_DELETES = 0

    # Subclasses use these to describe their unique characteristics
    model = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--chunk_size',
            default=self.DEFAULT_CHUNK_SIZE,
            type=int,
            help='Maximum number of expired tokens to delete in one transaction.'
        )
        parser.add_argument(
            '--sleep_between',
            default=self.DEFAULT_SLEEP_BETWEEN_DELETES,
            type=float,
            help='Seconds to sleep between chunked delete of expired tokens.'
        )

    def handle(self, *args, **options):
        raise CommandError("handle() called on abstract base class DeleteCommand!")

    def _handle(self, *_, **options):
        """
        Deletes expired tokens for the given model, chunking the deletes to avoid long table/row locks.
        """
        # Process the command arguments.
        chunk_size = options.get('chunk_size', self.DEFAULT_CHUNK_SIZE)
        if chunk_size <= 0:
            raise CommandError('Only positive chunk size is allowed ({}).'.format(chunk_size))
        sleep_between = options.get('sleep_between', self.DEFAULT_SLEEP_BETWEEN_DELETES)
        if sleep_between < 0:
            raise CommandError('Only non-negative sleep between seconds is allowed ({}).'.format(sleep_between))

        # These should only happen when called directly on base class, but just checking.
        if not self.model:
            raise CommandError('No model specified!')

        delete_date = timezone.now()

        total_expired_tokens = self.model.objects.filter(expires__lte=delete_date).count()

        if (total_expired_tokens == 0):
            log.info("SKIP - No expired %s tokens older than %s", self.model, delete_date)
            return

        ids = self.model.objects.filter(expires__lte=delete_date).aggregate(Min('id'), Max('id'))
        min_id = ids['id__min']
        max_id = ids['id__max']

        log.info(
            "STARTED: Deleting %s expired %s tokens older than '%s' w/ chunk size of %s and %s secs between chunks. "
            "Ids are %s - %s.",
            total_expired_tokens, self.model, delete_date, chunk_size, sleep_between, min_id, max_id
            )

        while True:
            log.info("Deleting up to %s expired tokens with id >= %s and id <= %s", chunk_size, min_id, min_id+chunk_size)
            with transaction.atomic():
                self.model.objects.filter(id__lte=min_id+chunk_size,
                                          id__gte=min_id,
                                          expires__lte=delete_date
                                         ).delete()

            min_id += chunk_size
            if min_id > max_id:
                break

            log.info("Sleeping %s seconds...", sleep_between)
            time.sleep(sleep_between)

        log.info("FINISHED: Deleted %s expired %s tokens total.", total_expired_tokens, self.model)
