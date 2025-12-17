from django.contrib import admin
from .models import Company, Stock, Dividend

admin.site.register(Company)
admin.site.register(Stock)
admin.site.register(Dividend)