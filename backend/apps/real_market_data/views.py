from django.shortcuts import render

# Create your views here.
from .tasks import download_data as dd
def download_data(request):
    dd.delay()
