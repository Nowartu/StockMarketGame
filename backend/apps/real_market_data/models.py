from django.contrib.postgres.fields import ArrayField
from django.db import models


class Company(models.Model):
    active = models.BooleanField(default=True)

    type = models.CharField(max_length=10)

    name = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=250)
    isin = models.CharField(max_length=100)
    market = models.CharField(max_length=10)
    submarket = models.CharField(max_length=50)
    sector = ArrayField(
        models.CharField(max_length=25)
    )
    stock_no = models.IntegerField()
    market_value = models.FloatField()
    value = models.FloatField()

    def __str__(self):
        return f'{self.name}'


class Stock(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()

    open_price = models.DecimalField(max_digits=12, decimal_places=4)
    close_price = models.DecimalField(max_digits=12, decimal_places=4)
    min_price = models.DecimalField(max_digits=12, decimal_places=4)
    max_price = models.DecimalField(max_digits=12, decimal_places=4)
    volume = models.IntegerField()
    transactions_no = models.IntegerField()
    turnover = models.BigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'date'],
                name='unique_company_daily_price'
            )
        ]

    def __str__(self):
        return f'{self.date} {self.company}'



class Dividend(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()

    value = models.DecimalField(max_digits=12, decimal_places=4)