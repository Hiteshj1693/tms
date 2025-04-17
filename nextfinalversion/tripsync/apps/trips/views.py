from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework import generics, permissions, status, serializers
from rest_framework.permissions import IsAuthenticated
from apps.trips.serializers import (
    TripSerializer,
    TripParticipantSerializer,
    TripJoinRequestActionSerializer,
    TripJoinRequestSerializer,
    UserSerializer,
)
from apps.trips.models import Trip, TripParticipant, TripJoinRequest, TripUserRelation
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.trips.permissions import (
    IsTripAdmin,
    IsTripOrganizer,
    IsTripOrganizerOrReadOnly,
)
from .emails import send_join_request_notification


class TripListCreateView(ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Trip.objects.filter(
            Q(trip_visibility="public")
            | Q(trip_organizer=user)
            | Q(participants__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(trip_organizer=self.request.user)


class TripDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsTripOrganizerOrReadOnly]


class TripParticipantCreateView(CreateAPIView):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]


class TripParticipantListView(ListAPIView):
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_id")
        return TripParticipant.objects.filter(trip_id=trip_id)


class TripParticipantUpdateView(RetrieveUpdateAPIView):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]


class TripParticipantDeleteView(DestroyAPIView):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        # Return a custom response
        return Response(
            {"message": "Trip participant deleted successfully!"},
            status=status.HTTP_200_OK,
        )


# 1. Submit a Trip Join Request
class TripJoinRequestCreateView(generics.CreateAPIView):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            join_request = serializer.save()
            send_join_request_notification(join_request)  # Notify trip admin via email
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)


# 2. Approve/Reject Join Request (Trip Admins only)
class TripJoinRequestActionView(generics.UpdateAPIView):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestActionSerializer
    permission_classes = [IsAuthenticated, IsTripOrganizer]

    def get_queryset(self):
        return TripJoinRequest.objects.filter(status="pending")


class TripJoinRequestDetailView(generics.UpdateAPIView):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestActionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTripOrganizer]
