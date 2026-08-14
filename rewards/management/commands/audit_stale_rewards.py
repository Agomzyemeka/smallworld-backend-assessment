import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from rewards.models import Reward


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Audit claimed rewards older than seven days and optionally expire them."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Mark stale claimed rewards as expired and set expires_at.",
        )

    def handle(self, *args, **options):
        fix = options["fix"]
        cutoff = timezone.now() - timedelta(days=7)

        stale = Reward.objects.filter(
            status="claimed",
            claimed_at__lt=cutoff,
        )

        total = stale.count()
        by_type = stale.values("reward_type").annotate(count=Count("id")).order_by("reward_type")

        self.stdout.write(f"Stale claimed rewards found: {total}")
        for row in by_type:
            self.stdout.write(f"  {row['reward_type']}: {row['count']}")

        if not fix:
            self.stdout.write("Dry run: no database changes made.")
            return

        expired_at = timezone.now()
        updated = 0
        batch = []

        # iterator() avoids caching the full queryset in application memory.
        for reward in stale.iterator(chunk_size=1000):
            reward.status = "expired"
            reward.expires_at = expired_at
            batch.append(reward)

            if len(batch) >= 1000:
                with transaction.atomic():
                    Reward.objects.bulk_update(
                        batch,
                        ["status", "expires_at"],
                        batch_size=1000,
                    )
                for reward in batch:
                    logger.info("Expired stale reward id=%s", reward.pk)
                updated += len(batch)
                batch.clear()

        if batch:
            with transaction.atomic():
                Reward.objects.bulk_update(
                    batch,
                    ["status", "expires_at"],
                    batch_size=1000,
                )
            for reward in batch:
                logger.info("Expired stale reward id=%s", reward.pk)
            updated += len(batch)

        self.stdout.write(f"Expired rewards updated: {updated}")
