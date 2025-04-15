# from django.db import models

# # Create your models here.

from django.db import models
from django.conf import settings
from apps.trips.models import Trip

User = settings.AUTH_USER_MODEL

class Expense(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses_paid")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="expenses_created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"


class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_split = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # optional

    def __str__(self):
        return f"{self.user} owes ₹{self.amount_owed} for '{self.expense.title}'"


class Settlement(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="settlements")
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settlements_made")
    paid_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settlements_received")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    settled_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.paid_by} paid ₹{self.amount} to {self.paid_to}"
