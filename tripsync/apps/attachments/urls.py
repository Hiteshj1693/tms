from rest_framework.routers import DefaultRouter
from .views import AttachmentViewSet

router = DefaultRouter()
router.register(r'', AttachmentViewSet, basename='attachments')

urlpatterns = router.urls



'''
 Postman Testing:
http
Copy
Edit
POST /attachments/
Content-Type: multipart/form-data
Authorization: Bearer <token>
Body:
- file: (select file)
- trip: 1
- description: "Hotel invoice"
'''