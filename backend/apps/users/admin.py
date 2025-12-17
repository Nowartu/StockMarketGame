from django.contrib import admin
from .models import UserProfile, UserStock

admin.site.register(UserProfile)
admin.site.register(UserStock)