from stocks.models import Instrument, Candle
from django.contrib.auth.models import User
from rest_framework import serializers


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['url', 'ticker', 'figi', 'name',
                  'currency', 'isin', 'lot', 'icon_url']


class CandleSerializer(serializers.ModelSerializer):
    o = serializers.FloatField(required=False)
    c = serializers.FloatField(required=False)
    h = serializers.FloatField(required=False)
    l = serializers.FloatField(required=False)
    v = serializers.IntegerField(required=False)
    time = serializers.DateTimeField(required=False)
    time__time = serializers.TimeField(required=False)

    class Meta:
        model = Candle
        #fields = '__all__'
        fields = ['o', 'c', 'h', 'l', 'v', 'time', 'time__time']

    def get_validation_exclusions(self):
        exclusions = super(CandleSerializer, self).get_validation_exclusions()
        return exclusions + ['o', 'c', 'h', 'l', 'v', 'time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
