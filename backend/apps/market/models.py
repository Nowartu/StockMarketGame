from django.contrib.postgres.fields import ArrayField
from django.db import models

class Company(models.Model):
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=250)
    sector = ArrayField(
        models.CharField(max_length=25),
        null=True
    )
    stock_no = models.IntegerField()
    market_value = models.FloatField()
    value = models.FloatField()

    class Meta:
        db_table = '"market"."company"'

    def __str__(self):
        return f'{self.full_name} ({self.name})'


class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(default=None, null=True)

    class OrderType(models.TextChoices):
        BUY = 'BUY', 'Buy'
        SELL = 'SELL', 'Sell'

    type = models.CharField(max_length=4, choices=OrderType.choices)

    amount = models.IntegerField()
    available = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    valid_to = models.DateTimeField()

    class Meta:
        db_table = '"market"."order"'

    def __str__(self):
        return f'{self.type} {self.amount} {self.user.nickname} {self.company.name}'


class Transaction(models.Model):
    order_1 = models.ForeignKey(Order, related_name="transactions1", on_delete=models.CASCADE)
    order_2 = models.ForeignKey(Order, related_name="transactions2", on_delete=models.CASCADE)

    amount = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=4)

    executed_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = '"market"."transaction"'

    def __str__(self):
        return f'{self.order_1} - {self.order_2}'
