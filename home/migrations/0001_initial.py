# Generated by Django 4.2.10 on 2024-02-09 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Policys",
            fields=[
                ("holder_name", models.CharField(max_length=60)),
                (
                    "policy_number",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("premuim", models.IntegerField()),
                ("coverage", models.IntegerField()),
                (
                    "policy_type",
                    models.CharField(
                        choices=[
                            ("health", "Health Insurance"),
                            ("life", "Life Insurance"),
                            ("auto", "Auto Insurance"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Policys",
            },
        ),
        migrations.CreateModel(
            name="Claims",
            fields=[
                (
                    "claim_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("policy_number", models.UUIDField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("A", "Accepted"),
                            ("R", "Rejected"),
                            ("I", "Initiated"),
                        ],
                        default="I",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("res_amt", models.IntegerField()),
                ("amt", models.IntegerField()),
                ("reason", models.TextField(default="----------")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Claims",
            },
        ),
    ]
