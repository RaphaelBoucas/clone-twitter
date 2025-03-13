# Generated by Django 5.1.6 on 2025-03-07 15:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("x", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Meep",
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
                ("body", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="tweets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
