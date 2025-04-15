# from django.shortcuts import render
# from apps.trips.serializers import TripActivitySerializer,TripInvitationSerializer,TripItinerarySerializer,TripJoinRequestSerializer,TripParticipantSerializer,TripSerializer
# from apps.trips.models import Trip,TripInvitation,TripActivity,TripItinerary,TripJoinRequest,TripParticipant
# from django.views import View
# from rest_framework import viewsets, permissions, status
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.views import APIView
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from .tasks import send_invitation_email
# from django.db.models import Q
# # Create your views here.

# class TripViewSet(viewsets.ModelViewSet):
#     # queryset = Trip.objects.all()
#     serializer_class = TripSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'admin':
#             return Trip.objects.all()
#         else:
#             return Trip.objects.filter( 
#                 Q(trip_visibility='public') |
#                 Q(trip_visibility='private', trip_organizer=user)
#             )


# class TripInvitationViewSet(viewsets.ModelViewSet):
#     queryset = TripInvitation.objects.all()
#     serializer_class = TripInvitationSerializer
#     permission_classes = [IsAuthenticated]

# class TripActivityViewSet(viewsets.ModelViewSet):
#     queryset = TripActivity.objects.all()
#     serializer_class = TripActivitySerializer
#     permission_classes = [IsAuthenticated]

# class TripItineraryViewSet(viewsets.ModelViewSet):
#     queryset = TripItinerary.objects.all()
#     serializer_class = TripItinerarySerializer
#     permission_classes = [IsAuthenticated]

# class TripJoinRequestViewSet(viewsets.ModelViewSet):
#     queryset = TripJoinRequest.objects.all()
#     serializer_class = TripJoinRequestSerializer
#     permission_classes = [IsAuthenticated]

# class TripParticipantViewSet(viewsets.ModelViewSet):
#     queryset = TripParticipant.objects.all()
#     serializer_class = TripParticipantSerializer
#     permission_classes = [IsAuthenticated]


from django.shortcuts import render
from apps.trips.serializers import TripActivitySerializer,TripInvitationSerializer,TripItinerarySerializer,TripJoinRequestSerializer,TripParticipantSerializer,TripSerializer
from apps.trips.models import Trip,TripInvitation,TripActivity,TripItinerary,TripJoinRequest,TripParticipant
from django.views import View
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.db.models import Q
from .tasks import send_invitation_email

# Create your views here.
# from rest_framework.throttling import UserRateThrottle
class TripViewSet(viewsets.ModelViewSet):
    # queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Trip.objects.all()
        else:
            return Trip.objects.filter( 
                Q(trip_visibility='public') |
                Q(trip_visibility='private', trip_organizer=user)
            )

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
    serializer_class = TripItinerary
    permission_classes = [IsAuthenticated]

class TripJoinRequestViewSet(viewsets.ModelViewSet):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequest
    permission_classes = [IsAuthenticated]

class TripParticipantViewSet(viewsets.ModelViewSet):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipant
    permission_classes = [IsAuthenticated]
