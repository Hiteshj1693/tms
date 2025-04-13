from rest_framework import serializers
from apps.trips.models import Trip, TripActivity, TripInvitation, TripItinerary, TripJoinRequest, TripParticipant
from datetime import date, datetime
from django.utils import timezone

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip 
        fields = "__all__"

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError("End date must be after start date.")
            if start_date < date.today():
                raise serializers.ValidationError("Start date must be today or a future date.")
        return data


class TripActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripActivity
        fields = "__all__"

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError("End time must be after start time.")
        return data


class TripInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripInvitation
        fields = "__all__"

    def validate_expired_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Expiration date must be in the future.")
        return value


class TripItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripItinerary
        fields = "__all__"

    def validate(self, data):
        trip = data.get('trip')
        itinerary_date = data.get('date')

        if trip and itinerary_date:
            if not (trip.start_date <= itinerary_date <= trip.end_date):
                raise serializers.ValidationError("Itinerary date must be within the trip date range.")
        return data


class TripJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripJoinRequest
        fields = "__all__"

    def validate(self, data):
        trip = data.get('trip')
        if trip and trip.trip_visibility == 'private':
            raise serializers.ValidationError("Join requests are not allowed for private trips.")
        return data


class TripParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripParticipant
        fields = "__all__"

    def validate(self, data):
        trip = data.get('trip')
        user = data.get('user')

        if trip and user:
            if trip.trip_visibility == 'private' and user != trip.trip_organizer:
                raise serializers.ValidationError("Only organizers can be added to private trips.")
        return data
