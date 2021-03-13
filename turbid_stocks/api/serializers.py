from stocks.models import Instrument
from django.contrib.auth.models import User
from rest_framework import serializers


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['ticker', 'figi', 'name',
                  'currency', 'isin', 'lot', 'icon_url']
