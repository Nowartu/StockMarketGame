from django.urls import path, include
from .views import OrderViewSet, CompanyList, TransactionList
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet, basename='order')
router.register(r'companies', CompanyList, basename="company")
router.register(r'transactions', TransactionList, basename="transaction")

urlpatterns = [
    path("", include(router.urls))
]