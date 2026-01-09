from django.contrib import admin
from .models import Company, Order, Transaction, Stock

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["active", "name", "full_name", "value"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'done', 'canceled', 'type', 'amount', 'available', 'price', 'created_at']
    list_filter = ['done', 'canceled']
    search_fields = ["user__nickname", 'company__name', "type"]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['date', 'company', 'open_price', 'close_price', 'min_price', 'max_price']
    list_filter = ['date']
    search_fields = ["company__name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["order_1__company", "order_1__user", "order_2__user", 'amount', 'price', 'executed_at']
