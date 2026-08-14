from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Reward",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.CharField(max_length=32)),
                ("claimed_at", models.DateTimeField()),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("reward_type", models.CharField(max_length=64)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["status", "claimed_at"], name="rewards_sta_claimed_3c8c2a_idx"),
                ],
            },
        ),
    ]
