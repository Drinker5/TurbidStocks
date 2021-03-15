from django.contrib import admin
from .models import Token, Instrument, Candle

# Register your models here.
admin.site.register(Token)
admin.site.register(Candle)
admin.site.register(Instrument)
