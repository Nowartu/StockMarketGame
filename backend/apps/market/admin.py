from django.contrib import admin
from .models import Company, Order, Transaction

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["active", "name", "full_name", "value"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['username', 'company_name', 'type', 'amount', 'price']

    def username(self, obj):
        return obj.user.nickname

    def company_name(self, obj):
        return obj.company.name

admin.site.register(Transaction)