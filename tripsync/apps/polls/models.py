# from django.db import models

# # Create your models here.

from django.db import models
from apps.trips.models import Trip
from apps.users.models import User
from datetime import timezone
# Create your models here.

class Poll(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='polls')
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_multiple_choice = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def has_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    votes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE,related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll','voted_by')

    def __str__(self):
        return f"{self.voted_by} voted on {self.poll}"
    