from rest_framework import serializers
from .models import Expense, ExpenseParticipant, Settlement
from apps.trips.models import Trip
from django.db import transaction

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Trip.participants.field.related_model.objects.all())

    class Meta:
        model = ExpenseParticipant
        fields = ['user', 'amount_owed', 'percentage_split']


class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True)
    paid_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Expense
        fields = ['id', 'trip', 'title', 'description', 'amount', 'paid_by', 'created_by', 'participants', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate(self, data):
        total_split = sum([p['amount_owed'] for p in data['participants']])
        if total_split != data['amount']:
            raise serializers.ValidationError("Total split amount must equal the expense amount.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        user = self.context['request'].user
        validated_data['created_by'] = user
        expense = Expense.objects.create(**validated_data)

        for participant in participants_data:
            ExpenseParticipant.objects.create(expense=expense, **participant)

        return expense


class ExpenseListSerializer(serializers.ModelSerializer):
    paid_by = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    participants = ExpenseParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'


class SettlementSerializer(serializers.ModelSerializer):
    paid_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Settlement
        fields = ['id', 'trip', 'paid_by', 'paid_to', 'amount', 'note', 'settled_at']
        read_only_fields = ['id', 'settled_at']
