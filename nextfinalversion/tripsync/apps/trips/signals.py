from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TripParticipant, TripUserRelation


@receiver(post_save, sender=TripParticipant)
def create_trip_user_relation(sender, instance, created, **kwargs):
    if created:
        trip = instance.trip
        user = instance.user
        if trip.trip_organizer == user:
            TripUserRelation.objects.get_or_create(
                trip_id=trip, user_id=user, defaults={"user_role": "trip_admin"}
            )
        else:
            TripUserRelation.objects.update_or_create(
                trip_id=trip, user_id=user, defaults={"user_role": "participant"}
            )
