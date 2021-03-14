from stocks.models import Instrument
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, filters
from .serializers import InstrumentSerializer, UserSerializer


class InstrumentViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r'[\w\d\@.]+'
    serializer_class = InstrumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Instrument.objects.all()
    search_fields = ['^ticker', 'name']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering = ['ticker']
    ordering_fields = ['name']


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
