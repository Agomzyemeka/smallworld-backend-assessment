from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from rewards.models import Reward


class AuditStaleRewardsCommandTests(TestCase):
    def setUp(self):
        now = timezone.now()
        Reward.objects.create(
            status="claimed",
            claimed_at=now - timedelta(days=8),
            reward_type="cash",
        )
        Reward.objects.create(
            status="claimed",
            claimed_at=now - timedelta(days=2),
            reward_type="cash",
        )
        Reward.objects.create(
            status="expired",
            claimed_at=now - timedelta(days=10),
            reward_type="cash",
        )

    def test_default_is_a_dry_run(self):
        call_command("audit_stale_rewards")

        reward = Reward.objects.order_by("id").first()
        self.assertEqual(reward.status, "claimed")
        self.assertIsNone(reward.expires_at)

    def test_fix_expires_only_stale_claimed_rewards(self):
        call_command("audit_stale_rewards", "--fix")

        rewards = list(Reward.objects.order_by("id"))
        self.assertEqual(rewards[0].status, "expired")
        self.assertIsNotNone(rewards[0].expires_at)
        self.assertEqual(rewards[1].status, "claimed")
        self.assertIsNone(rewards[1].expires_at)
        self.assertEqual(rewards[2].status, "expired")
