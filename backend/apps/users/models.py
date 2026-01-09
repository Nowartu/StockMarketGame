from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    nickname = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    blocked_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username} ({self.nickname})'

    class Meta:
        db_table = '"user"."userprofile"'

class UserStock(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="userstock")
    company = models.ForeignKey("market.Company", on_delete=models.CASCADE, related_name="userstock")
    amount = models.IntegerField()
    blocked = models.IntegerField()

    class Meta:
        db_table = '"user"."userstock"'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'user'],
                name='unique_user_company'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.company}'