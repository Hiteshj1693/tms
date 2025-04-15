from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet

router = DefaultRouter()
router.register(r'', FeedbackViewSet, basename='feedback')

urlpatterns = router.urls


'''
POST /feedback/
{
  "type": "trip",
  "trip": 1,
  "rating": 4,
  "comments": "Loved the experience, thanks to the trip admins!"
}

'''