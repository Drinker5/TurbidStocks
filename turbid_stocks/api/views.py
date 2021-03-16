from stocks.models import Instrument, Candle
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from rest_framework import filters, permissions, serializers, viewsets
from .serializers import InstrumentSerializer, CandleSerializer, UserSerializer
from stocks.views import sync_candles
from rest_framework.pagination import PageNumberPagination


class InstrumentViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r'[\w\d\@.]+'
    serializer_class = InstrumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Instrument.objects.all()
    search_fields = ['^ticker', 'name']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering = ['ticker']
    ordering_fields = ['name']


class CandleSetPagination(PageNumberPagination):
    page_size = 100000


class CandleViewSet(viewsets.ModelViewSet):
    serializer_class = CandleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['interval', 'figi']
    ordering = ['time']
    pagination_class = CandleSetPagination

    def get_queryset(self):
        queryset = Candle.objects.all()
        figi = self.request.query_params.get('figi', None)
        if figi is None:
            raise serializers.ValidationError('figi empty')
        queryset = queryset.filter(figi=figi)
        interval = self.request.query_params.get('interval', None)
        if interval is None:
            raise serializers.ValidationError('interval empty')
        queryset = queryset.filter(interval=interval)
        from_ = self.request.query_params.get('from', None)
        if from_ is None:
            raise serializers.ValidationError('from empty')
        to = self.request.query_params.get('to', None)
        if to is None:
            raise serializers.ValidationError('to empty')
        queryset = queryset.filter(time__range=[from_, to])

        sync_candles(figi, parse_datetime(from_), parse_datetime(to), interval)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
