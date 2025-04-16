from django.shortcuts import render
from apps.trips.serializers import TripActivitySerializer,TripInvitationSerializer,TripItinerarySerializer,TripJoinRequestSerializer,TripParticipantSerializer,TripSerializer
from apps.trips.models import Trip,TripInvitation,TripActivity,TripItinerary,TripJoinRequest,TripParticipant
from django.views import View
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.db.models import Q
from .tasks import send_invitation_email
from apps.trips.permissions import IsTripOrganizerOrReadOnly

# Create your views here.
# from rest_framework.throttling import UserRateThrottle
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]
    permission_classes = [IsTripOrganizerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(trip_organizer=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'admin':
    #         return Trip.objects.all()
    #     else:
    #         return Trip.objects.filter( 
    #             Q(trip_visibility='public') |
    #             Q(trip_visibility='private', trip_organizer=user)
    #         )

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Trip.objects.filter(
                Q(trip_visibility='public') |
                Q(trip_organizer=user) |
                Q(participants__user=user)
            ).distinct()
        return Trip.objects.filter(trip_visibility='public')

# class TripParticipantListView(RetrieveAPIView):
#     permission_classes = [IsAuthenticated, IsAdminOrTripParticipant]


class TripInvitationViewSet(viewsets.ModelViewSet):
    queryset = TripInvitation.objects.all()
    serializer_class = TripInvitationSerializer
    permission_classes = [IsAuthenticated]

class TripActivityViewSet(viewsets.ModelViewSet):
    queryset = TripActivity.objects.all()
    serializer_class = TripActivitySerializer
    permission_classes = [IsAuthenticated]

class TripItineraryViewSet(viewsets.ModelViewSet):
    queryset = TripItinerary.objects.all()
    serializer_class = TripItinerarySerializer
    permission_classes = [IsAuthenticated]

class TripJoinRequestViewSet(viewsets.ModelViewSet):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestSerializer
    permission_classes = [IsAuthenticated]

class TripParticipantViewSet(viewsets.ModelViewSet):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]

