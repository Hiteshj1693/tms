from rest_framework import serializers
from apps.trips.models import Trip, TripActivity, TripInvitation, TripItinerary, TripJoinRequest, TripParticipant
from datetime import date
class TripSerializer(serializers.ModelSerializer):
    # participants = serializers.StringRelatedField(many=True, read_only=True)
    participants = serializers.SerializerMethodField()
    class Meta:
        model = Trip 
        # fields = "__all__"
        fields = [
            "id", "participants", "trip_title", "trip_description",
            "trip_destination", "start_date", "end_date",
            "trip_visibility", "trip_image", "created_at",
            "updated_at", "trip_organizer"
        ]
        read_only_fields = ['trip_organizer', 'created_at', 'updated_at']

    # def get_participants(self, obj):
    #     request = self.context.get("request")
    #     user = request.user if request else None

    #     # Check if user is admin, organizer, or participant
    #     if user and (user.is_staff or user == obj.trip_organizer or user in obj.participants.all()):
    #         organizer_email = obj.trip_organizer.email
    #         return [
    #             f"{participant.email} in {obj.trip_title} ({organizer_email})"
    #             for participant in obj.participants.all()
    #         ]
    #     return None  # Hide participants if not permitted
    def get_participants(self, obj):
        user = self.context['request'].user
        organizer_email = obj.trip_organizer.email

        # Check if user is organizer or a participant
        if user == obj.trip_organizer or TripParticipant.objects.filter(user=user, trip=obj).exists():
            # Use the TripParticipant relation
            return [
                f"{participant.user.email} in ({organizer_email})"
                for participant in obj.participants.all()
            ]
        return None


    def validate(self, data):
        start_date = data.get('start_date', self.instance.start_date if self.instance else None)
        end_date = data.get('end_date', self.instance.end_date if self.instance else None)

        if start_date and start_date < date.today():
            raise serializers.ValidationError("Start date must be today or a future date.")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after start date.")
        return data

class TripActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripActivity
        fields = "__all__"

class TripInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripInvitation
        fields = "__all__"

class TripItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripItinerary
        fields = "__all__"

class TripJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripJoinRequest
        fields = "__all__"

class TripParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripParticipant
        fields = "__all__"