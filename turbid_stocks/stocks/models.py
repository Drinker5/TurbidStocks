from django.db import models

# Create your models here.
INTERVALS = [("1min", "1min"),
             ("2min", "2min"),
             ("3min", "3min"),
             ("5min", "5min"),
             ("10min", "10min"),
             ("15min", "15min"),
             ("30min", "30min"),
             ("hour", "hour"),
             ("day", "day"),
             ("week", "week"),
             ("month", "month")]


class Candle(models.Model):
    figi = models.CharField(max_length=12)
    interval = models.CharField(choices=INTERVALS, max_length=10)
    o = models.FloatField()
    c = models.FloatField()
    h = models.FloatField()
    l = models.FloatField()
    v = models.FloatField()
    time = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['figi', 'interval'],
                         name='figi_interval_idx'),
            models.Index(fields=['figi', 'interval', 'time'],
                         name='unique_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['figi', 'interval', 'time'],
                                    name='unique_candle')
        ]

    def __str__(self):
        return f"{self.figi}-{self.interval}-{self.time}"


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
