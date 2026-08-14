from django.db import models


class Reward(models.Model):
    """Minimal assessment model matching the fields specified in Q8."""

    status = models.CharField(max_length=32)
    claimed_at = models.DateTimeField()
    expires_at = models.DateTimeField(null=True, blank=True)
    reward_type = models.CharField(max_length=64)

    class Meta:
        indexes = [
            models.Index(fields=["status", "claimed_at"]),
        ]
