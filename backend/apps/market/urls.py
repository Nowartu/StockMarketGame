from django.urls import path, include
from .views import UserViewSet, GroupViewSet, OrderViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"orders", OrderViewSet, basename='order')

urlpatterns = [
    path("", include(router.urls)),
]