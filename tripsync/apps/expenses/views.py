# from django.shortcuts import render

# # Create your views here.

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Expense, Settlement
from .serializers import (
    ExpenseSerializer,
    ExpenseListSerializer,
    SettlementSerializer,
)
from apps.trips.models import Trip
from rest_framework.exceptions import PermissionDenied


class IsTripParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.trip.participants.all() or request.user == obj.trip.created_by


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExpenseListSerializer
        return ExpenseSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTripParticipant()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        trip = serializer.validated_data.get('trip')
        if self.request.user not in trip.participants.all() and self.request.user != trip.created_by:
            raise PermissionDenied("You are not a participant of this trip.")
        serializer.save()


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        trip = serializer.validated_data.get('trip')
        if self.request.user not in trip.participants.all() and self.request.user != trip.created_by:
            raise PermissionDenied("You are not allowed to settle in this trip.")
        serializer.save()
