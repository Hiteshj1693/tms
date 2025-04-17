# Generated by Django 5.1.8 on 2025-04-15 20:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0002_remove_tripparticipant_role"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="trip_participants",
            field=models.ManyToManyField(
                blank=True, related_name="joined_trips", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
