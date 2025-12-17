from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    blocked_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username} ({self.nickname})'

class UserStock(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.ForeignKey("market.Company", on_delete=models.CASCADE)
    amount = models.IntegerField()
    available = models.IntegerField()