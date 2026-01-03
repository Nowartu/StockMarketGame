from django.urls import path, include
from .views import OrderViewSet, CompanyViewSet, TransactionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet, basename='order')
router.register(r"companies", CompanyViewSet, basename='company')
router.register(r"transactions", TransactionViewSet, basename='transaction')

urlpatterns = [
    path("", include(router.urls)),
]