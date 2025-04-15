# from django.db import models

# # Create your models here.

from django.db import models
from apps.users.models import User
from apps.trips.models import Trip

class Attachment(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='trip_attachments/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} by {self.uploaded_by}"
