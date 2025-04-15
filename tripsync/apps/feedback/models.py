# from django.db import models

# # Create your models here.

from django.db import models
from apps.users.models import User
from apps.trips.models import Trip

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('trip', 'Trip Experience'),
        ('organizer', 'Trip Organizer'),
        ('system', 'System Feedback'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    rating = models.PositiveIntegerField(null=True, blank=True)  # Optional for 'system'
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} feedback from {self.user}"
