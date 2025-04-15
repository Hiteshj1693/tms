# # from django.shortcuts import render

# # # Create your views here.

# # from django.shortcuts import render
# # from apps.polls.models import Poll, PollOption, Vote
# # from apps.polls.serializers import PollSerializer, PollOptionSerializer, VoteSerializer
# # from rest_framework import generics
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework.response import Response
# # # Create your views here.

# # class PollList(generics.ListCreateAPIView):
# #     queryset = Poll.objects.all()
# #     serializer_class = [PollSerializer]
# #     permission_classes = [IsAuthenticated]
    
# #     def list(self,request):
# #         queryset = self.get_queryset()
# #         serializer = PollSerializer(queryset, many = True)
# #         return Response(serializer.data)

# from rest_framework import viewsets, generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from apps.polls.models import Poll, PollOption, Vote
# from apps.polls.serializers import PollSerializer, PollOptionSerializer, VoteSerializer
# from django.utils import timezone

# class PollViewSet(viewsets.ModelViewSet):
#     serializer_class = PollSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Poll.objects.filter(trip__participants__user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

# class PollOptionViewSet(viewsets.ModelViewSet):
#     serializer_class = PollOptionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return PollOption.objects.filter(poll__trip__participants__user=self.request.user)

# class VoteAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         option_id = request.data.get("option")
#         try:
#             option = PollOption.objects.get(id=option_id)
#         except PollOption.DoesNotExist:
#             return Response({"error": "Option not found"}, status=404)

#         # Prevent duplicate votes by user on same poll
#         if Vote.objects.filter(user=request.user, option__poll=option.poll).exists():
#             return Response({"error": "You have already voted"}, status=400)

#         if option.poll.expires_at < timezone.now():
#             return Response({"error": "Poll has expired"}, status=400)

#         vote = Vote.objects.create(user=request.user, option=option)
#         return Response(VoteSerializer(vote).data, status=201)



from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Poll, PollOption, Vote
from .serializers import (
    PollCreateSerializer,
    PollDetailSerializer,
    PollOptionSerializer,
    VoteCreateSerializer,
    VoteUpdateSerializer,
    VoteSerializer,
)
from .permissions import IsPollCreatorOrReadOnly


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated, IsPollCreatorOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PollCreateSerializer
        return PollDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def close(self, request, pk=None):
        """Manually close a poll (admin/creator only)"""
        poll = self.get_object()
        if poll.created_by != request.user:
            return Response({'detail': 'Only the poll creator can close the poll.'}, status=403)
        poll.is_active = False
        poll.save()
        return Response({'detail': 'Poll closed successfully.'})


# class VoteViewSet(viewsets.ModelViewSet):
#     queryset = Vote.objects.all()
#     permission_classes = [IsAuthenticated]

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return VoteCreateSerializer
#         elif self.action in ['update', 'partial_update']:
#             return VoteUpdateSerializer
#         return VoteSerializer

#     def get_queryset(self):
#         return Vote.objects.filter(voted_by=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(voted_by=self.request.user)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

