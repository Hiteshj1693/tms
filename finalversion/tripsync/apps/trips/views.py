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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_join_request(request, request_id):
    try:
        join_request = TripJoinRequest.objects.get(id=request_id, user=request.user)

        if join_request.status != "pending":
            return Response({"error": "Request already processed"}, status=400)

        action = request.data.get("action")  # 'accept' or 'reject'

        if action == "accept":
            join_request.status = "approved"
            TripParticipant.objects.create(user=request.user, trip=join_request.trip)
        elif action == "reject":
            join_request.status = "rejected"
        else:
            return Response({"error": "Invalid action"}, status=400)

        join_request.save()
        return Response({"message": f"Request {action}ed successfully."})

    except TripJoinRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_join_request(request, request_id):
    try:
        join_request = TripJoinRequest.objects.get(id=request_id, user=request.user)

        if join_request.status != "pending":
            return Response({"error": "Request already processed"}, status=400)

        action = request.data.get("action")  # 'accept' or 'reject'

        if action == "accept":
            join_request.status = "approved"
            TripParticipant.objects.create(user=request.user, trip=join_request.trip)
        elif action == "reject":
            join_request.status = "rejected"
        else:
            return Response({"error": "Invalid action"}, status=400)

        join_request.save()
        return Response({"message": f"Request {action}ed successfully."})

    except TripJoinRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)


def send_email_to_user(email, trip, join_request):
    # This is just a mock. Integrate with Django Email backend
    subject = f"Invitation to join Trip: {trip.trip_title}"
    accept_url = f"http://yourfrontend.com/trip/join/{join_request.id}/?action=accept"
    reject_url = f"http://yourfrontend.com/trip/join/{join_request.id}/?action=reject"
    body = f"""
    You have been invited to join the trip: {trip.trip_title}.
    
    Message from inviter: {join_request.message}

    Accept: {accept_url}
    Reject: {reject_url}
    """
    print(f"Send email to {email}:\n{body}")


@api_view(['GET'])
@permission_classes([AllowAny])  # Can be changed to token-based for secure APIs
def trip_join_response(request, request_id):
    action = request.GET.get('action')  # 'accept' or 'reject'
    try:
        join_request = TripJoinRequest.objects.get(id=request_id)

        if join_request.status != "pending":
            return Response({"message": "Request already processed."})

        if action == "accept":
            TripParticipant.objects.create(user=join_request.user, trip=join_request.trip)
            join_request.status = "approved"
        elif action == "reject":
            join_request.status = "rejected"
        else:
            return Response({"error": "Invalid action"}, status=400)

        join_request.save()
        return Response({"message": f"Successfully {action}ed the trip invitation."})

    except TripJoinRequest.DoesNotExist:
        return Response({"error": "Join request not found"}, status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
def trip_join_response(request, request_id):
    action = request.GET.get('action')
    try:
        join_request = TripJoinRequest.objects.get(id=request_id)

        if join_request.status != "pending":
            return Response({"message": "Request already processed."})

        if action == "accept":
            # Add to TripParticipant
            TripParticipant.objects.create(user=join_request.user, trip=join_request.trip)

            # Add to TripUserRelation with role as 'participant'
            TripUserRelation.objects.create(
                trip_id=join_request.trip,
                user_id=join_request.user,
                user_role='participant'
            )

            join_request.status = "approved"

        elif action == "reject":
            join_request.status = "rejected"
        else:
            return Response({"error": "Invalid action"}, status=400)

        join_request.save()
        return Response({"message": f"Successfully {action}ed the trip invitation."})

    except TripJoinRequest.DoesNotExist:
        return Response({"error": "Join request not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
