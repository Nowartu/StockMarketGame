from django.contrib import admin
from .models import Company, Order, Transaction

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["active", "name", "full_name", "value"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'done', 'canceled', 'type', 'amount', 'available', 'price', 'created_at']
    list_filter = ['done', 'canceled']
    search_fields = ["user__nickname", 'company__name', "type"]

admin.site.register(Transaction)