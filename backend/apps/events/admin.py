from django.contrib import admin
from .models import Event

# Register your models here.

@admin.register(Event)
class AdminEvent(admin.ModelAdmin):
    list_display = ['created_at', 'type', 'source', 'reference_id', 'payload']
    list_filter = ['created_at', 'source', 'type']
    list_display_links = list_display


