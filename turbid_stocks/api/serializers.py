from stocks.models import Instrument, Candle
from django.contrib.auth.models import User
from rest_framework import serializers


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['url', 'ticker', 'figi', 'name',
                  'currency', 'isin', 'lot', 'icon_url']


class CandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = ['o', 'c', 'h', 'l', 'v', 'time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
