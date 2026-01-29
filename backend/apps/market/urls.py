from django.urls import path, include
from .views import OrderViewSet, CompanyList, TransactionList, ProfileList, UserStockList, StockList, BucketViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet, basename='order')
router.register(r'companies', CompanyList, basename="company")
router.register(r'transactions', TransactionList, basename="transaction")
router.register(f'profile', ProfileList, basename="profile")
router.register(f'userstocks', UserStockList, basename='userstock')
router.register(f'stocks', StockList, basename="stock")
router.register(f'buckets', BucketViewSet, basename="bucket")

urlpatterns = [
    path("", include(router.urls))
]