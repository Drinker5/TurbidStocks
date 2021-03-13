from django.db import models

# Create your models here.


class Token(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.key


CURRENCIES = [("RUB", "RUB"), ("USD", "USD"), ("EUR", "EUR")]


class Instrument(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    figi = models.CharField(max_length=12)
    isin = models.CharField(max_length=12)
    name = models.CharField(max_length=100)
    currency = models.CharField(choices=CURRENCIES, max_length=3)
    lot = models.IntegerField(default=1)

    def icon_url(self):
        size = 40  # 20 40 160 640
        return f"http://static.tinkoff.ru/brands/traiding/{self.isin}x{size}.png"

    def __str__(self) -> str:
        return self.ticker

# class Currency(models.Model):
    #id = models.CharField(max_length=3)
