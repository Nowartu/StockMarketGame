from django.contrib import admin
from .models import UserProfile, UserStock

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'user', 'balance', 'blocked_balance']

    def user(self):
        return self.user.username

@admin.register(UserStock)
class UserStockAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'amount', 'blocked']

    def user(self):
        return self.user.nickname

    def company(self):
        return self.company.name