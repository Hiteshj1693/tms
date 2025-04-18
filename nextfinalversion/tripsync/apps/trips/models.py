# from django.db import models
# from apps.users.models import User
# # Create your models here.
# from django.conf import settings
# from django.utils import timezone
# import uuid
# from datetime import date, datetime
# from django.core.exceptions import ValidationError

# # User = settings.AUTH_USER_MODEL

# class Trip(models.Model):
#     VISIBILITY_CHOICES = [
#         ('private','Private'),
#         ('public','Public'),
#     ]

#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     trip_organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_trip')
#     trip_title = models.CharField(max_length=255)
#     trip_description = models.TextField(blank=True)
#     trip_destination = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     trip_visibility = models.CharField(max_length=10,choices=VISIBILITY_CHOICES, default='private')
#     trip_image = models.ImageField(upload_to='trip_images/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     trip_participants = models.ManyToManyField(User, related_name='joined_trips', blank=True)

#     def clean(self):
#         if self.end_date < self.start_date:
#             raise ValidationError("End Date is always greater than Start Date, So enter Valid date")

#         if self.start_date < date.today():
#             raise ValidationError("Start date must be today or any future date")

#     def __str__(self):
#         return f"{self.trip_title} ({self.trip_organizer})"


# class TripParticipant(models.Model):
#     # ROLE_CHOICES = [
#     #     ('participant','Participant'),
#     #     ('coorganizer','Co-Organizer'),
#     # ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='participants')
#     # role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
#     joined_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('trip', 'user')

#     def clean(self):
#         if self.trip.trip_visibility == 'private' and self.user != self.trip.trip_organizer:
#             raise ValidationError("This trip for only organizers")


#     def __str__(self):
#         return f"{self.user} in {self.trip}"


# class TripItinerary(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itineraries')
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     date = models.DateField()

#     def clean(self):
#         if not (self.trip.start_date <= self.date <= self.trip.end_date):
#             raise ValidationError("Date must be within trip dates")

#     def __str__(self):
#         return f"Itinerary: {self.title} on {self.date}"


# class TripActivity(models.Model):
#     itinerary = models.ForeignKey(TripItinerary, on_delete=models.CASCADE,related_name='activities')
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     location = models.CharField(max_length=255, blank=True)

#     def clean(self):
#         if self.end_time < self.start_time:
#             raise ValidationError("End Date is always greater than Start Date, So enter Valid date")

#     def __str__(self):
#         return f"Trip Activity : {self.title} at {self.start_time}"


# class TripJoinRequest(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_join_requests')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField(blank=True)
#     status = models.CharField(max_length=10, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')],default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('trip', 'user')

#     def clean(self):
#         if self.trip.trip_visibility == 'private':
#             raise ValidationError("This request is only for organizers, so this is private request")

#     def __str__(self):
#         return f"TripJoinRequest: {self.user}, to {self.trip} ({self.status})"

# class TripInvitation(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='invitations')
#     email = models.EmailField()
#     invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     status = models.CharField(max_length=10, choices=[('pending','Pending'),('accepted','Accepted'),('expired','Expired')], default='pending')
#     invited_at = models.DateTimeField(auto_now_add=True)
#     expired_at = models.DateTimeField()

#     def is_expired(self):
#         return timezone.now() > self.expired_at

#     def clean(self):
#         if self.expired_at <= timezone.now():
#             raise ValidationError("Expired must be in the future")

#     def __str__(self):
#         return f"Invited to {self.email} for {self.trip} ({self.status})"


# class TripUserRelation(models.Model):
#     ROLE_CHOICE = [
#         ('admin','Admin'),
#         ('trip_admin','Trip Admin'),
#         ('participant','Trip Participant'),
#         ('viewer','Viewer'),
#         ('guest','Guest'),
#     ]
#     trip_id = models.ForeignKey(Trip,on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     user_role = models.CharField(max_length=20,choices=ROLE_CHOICE,default="guest")


# # ?batch mail, concorrent, time.sleep, context switching,
# # celery task
# # nested celery task
# # batch


# '''
# In this if trip is public than viewer can choose their trip and viewer and guest can see all the trips and if want to appear in trip user can send than mail to trip admin if trip admin accept that invitation than and than only user become participant of the trip, but if trip is private than trip admin send the mail or any notification to the user who trip admin want to send invitation, if user accept that invitation than they can be a part of that private trip
# '''


from django.db import models
from apps.users.models import User

# Create your models here.
from django.conf import settings
from django.utils import timezone
import uuid
from datetime import date, datetime
from django.core.exceptions import ValidationError


class Trip(models.Model):
    VISIBILITY_CHOICES = [
        ("private", "Private"),
        ("public", "Public"),
    ]
    trip_organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organized_trip"
    )
    trip_title = models.CharField(max_length=255)
    trip_description = models.TextField(blank=True)
    trip_destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default="private"
    )
    trip_image = models.ImageField(upload_to="trip_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    trip_participants = models.ManyToManyField(
        User, related_name="joined_trips", blank=True
    )
    
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                "End Date is always greater than Start Date, So enter Valid date"
            )

        if self.start_date < date.today():
            raise ValidationError("Start date must be today or any future date")

    def __str__(self):
        return f"{self.trip_title} ({self.trip_organizer})"


class TripParticipant(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="participants"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trip", "user")

    def clean(self):
        if (
            self.trip.trip_visibility == "private"
            and self.user != self.trip.trip_organizer
        ):
            raise ValidationError("This trip for only organizers")

    def __str__(self):
        return f"{self.user} in {self.trip}"


class TripUserRelation(models.Model):
    ROLE_CHOICE = [
        ("admin", "Admin"),
        ("trip_admin", "Trip Admin"),
        ("participant", "Trip Participant"),
        ("viewer", "Viewer"),
        ("guest", "Guest"),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICE, default="guest")


class TripJoinRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    trip = models.ForeignKey(
        "Trip", on_delete=models.CASCADE, related_name="trip_join_requests"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trip", "user")  # Prevent duplicate join requests

    def clean(self):
        # Prevent join request to private trips if user is neither organizer nor participant
        from .models import TripUserRelation

        if self.trip.trip_visibility == "private":
            is_member = TripUserRelation.objects.filter(
                trip=self.trip, user=self.user
            ).exists()

            if not is_member:
                raise ValidationError(
                    "You can't request to join a private trip you're not a part of."
                )

    def __str__(self):
        return f"JoinRequest: {self.user.username} → {self.trip.trip_title} [{self.status}]"
