"""Alter Video model fields to be optional.

This migration makes the ``titulo`` field optional (allowing blank
titles) and the ``usuario`` foreign key nullable so that videos can be
uploaded without being associated with a user account.  It depends on
the initial migration that created the ``Video`` model.
"""

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="titulo",
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name="video",
            name="usuario",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
            ),
        ),
    ]