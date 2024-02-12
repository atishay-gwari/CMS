# Generated by Django 4.2.10 on 2024-02-12 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="claims",
            name="status",
            field=models.CharField(
                choices=[
                    ("Accepted", "Accepted"),
                    ("Rejected", "Rejected"),
                    ("Initiated", "Initiated"),
                ],
                default="I",
                max_length=20,
            ),
        ),
    ]
