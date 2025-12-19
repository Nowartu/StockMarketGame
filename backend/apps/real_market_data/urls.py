from django.urls import path
from .views import download_data

urlpatterns = [
    path("", download_data),
]