from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Expense
from apps.notifications.models import Notification

@receiver(post_save, sender=Expense)
def notify_split_expense(sender, instance, created, **kwargs):
    if created:
        for user in instance.split_between.all():
            if user != instance.paid_by:
                Notification.objects.create(
                    recipient=user,
                    message=f"You were included in an expense: '{instance.title}'",
                    trip=instance.trip
                )
