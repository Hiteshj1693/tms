from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, SettlementViewSet

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'settlements', SettlementViewSet, basename='settlement')

urlpatterns = [
    path('', include(router.urls)),
]


'''
{
  "trip": 1,
  "title": "Dinner at Goa Beach",
  "amount": 3000,
  "paid_by": 2,
  "split_between": [2, 3, 4],
  "description": "Dinner split among friends"
}

'''