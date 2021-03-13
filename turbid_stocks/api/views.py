from stocks.models import Instrument
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, filters
from .serializers import InstrumentSerializer


class InstrumentViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r'[\w\d\@.]+'
    serializer_class = InstrumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Instrument.objects.all()
    search_fields = ['^ticker', 'name']
    filter_backends = [filters.SearchFilter]
