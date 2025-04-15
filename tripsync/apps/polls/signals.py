# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vote, PollOption

@receiver(post_save, sender=Vote)
def update_votes_count_on_save(sender, instance, created, **kwargs):
    if created:
        option = instance.option
        option.votes_count = option.votes.count()
        option.save()

@receiver(post_delete, sender=Vote)
def update_votes_count_on_delete(sender, instance, **kwargs):
    option = instance.option
    option.votes_count = option.votes.count()
    option.save()
