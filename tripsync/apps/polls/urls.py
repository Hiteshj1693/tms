# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PollViewSet, PollOptionViewSet, VoteAPIView

# router = DefaultRouter()
# router.register(r'polls', PollViewSet,basename='poll')
# router.register(r'poll-options', PollOptionViewSet,basename='poll-option')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('vote/', VoteAPIView.as_view(), name='vote'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]
