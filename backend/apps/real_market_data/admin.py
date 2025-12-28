from django.contrib import admin
from .models import Company, Stock, Dividend

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['date', 'company', 'open_price', 'close_price', 'min_price', 'max_price']
    list_filter = ['date']
    search_fields = ["company__name"]

admin.site.register(Dividend)