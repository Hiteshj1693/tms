@shared_task
def auto_close_poll(poll_id):
    poll = Poll.objects.get(id=poll_id)
    if timezone.now() >= poll.end_time:
        poll.is_active = False
        poll.save()



# views.py

class MyVotesView(generics.ListAPIView):
    serializer_class = VoteSerializer

    def get_queryset(self):
        return Vote.objects.filter(voted_by=self.request.user)


# urls.py

path('my-votes/', MyVotesView.as_view(), name='my-votes'),
