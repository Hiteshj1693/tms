from django.contrib import admin
from apps.trips.models import Trip, TripParticipant, TripJoinRequest, TripUserRelation

# Register your models here.

admin.site.register(Trip)
admin.site.register(TripUserRelation)
admin.site.register(TripJoinRequest)
admin.site.register(TripParticipant)
