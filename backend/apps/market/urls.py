from django.urls import path, include
from .views import OrderViewSet, CompanyList, TransactionList, ProfileList, UserStockList, StockList
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet, basename='order')
router.register(r'companies', CompanyList, basename="company")
router.register(r'transactions', TransactionList, basename="transaction")
router.register(f'profile', ProfileList, basename="profile")
router.register(f'userstock', UserStockList, basename='userstock')
router.register(f'stock', StockList, basename="stock")

urlpatterns = [
    path("", include(router.urls))
]