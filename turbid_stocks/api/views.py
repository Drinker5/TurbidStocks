from stocks.models import Instrument, Candle
from stocks.views import sync_candles
from .serializers import InstrumentSerializer, CandleSerializer, UserSerializer
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters, permissions, serializers, viewsets
from rest_framework.pagination import PageNumberPagination
import datetime


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
    page_size = 10000


class CandleViewSet(viewsets.ModelViewSet):
    serializer_class = CandleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['interval', 'figi']
    ordering = ['time']
    pagination_class = CandleSetPagination
    queryset = Candle.objects.all()

    def sync(self, figi, interval, from_, to):
        today = datetime.datetime.today().date()
        if today < parse_datetime(to).date():
            to = today.strftime("%Y-%m-%dT00:00:00.000Z")

        sync_candles(figi, parse_datetime(from_), parse_datetime(to), interval)

    def list(self, request):
        candles = Candle.objects.all()
        figi = request.query_params.get('figi', None)
        if figi is None:
            raise serializers.ValidationError('figi empty')
        interval = request.query_params.get('interval', None)
        if interval is None:
            raise serializers.ValidationError('interval empty')
        from_ = request.query_params.get('from', None)
        if from_ is None:
            raise serializers.ValidationError('from empty')
        to = request.query_params.get('to', None)
        if to is None:
            raise serializers.ValidationError('to empty')

        self.sync(figi, interval, from_, to)
        candles = candles.filter(
            figi=figi, interval=interval, time__range=[from_, to])

        hours = request.query_params.getlist('hours', None)
        minutes = request.query_params.getlist('minutes', None)
        if len(hours) > 0 and len(minutes) > 0 and len(hours) == len(minutes):
            i = 0
            times = []
            while i < len(hours):
                times.append(datetime.time(
                    hour=int(hours[i]), minute=int(minutes[i])))
                i = i + 1
            candles = candles.filter(time__time__in=times)
        else:
            if len(hours) > 0:
                candles = candles.filter(time__hour__in=hours)
            if len(minutes) > 0:
                candles = candles.filter(time__minute__in=minutes)

        page = self.paginate_queryset(candles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(candles, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def group_candles(self, request):
        candles = Candle.objects.all()
        figi = request.query_params.get('figi', None)
        if figi is None:
            raise serializers.ValidationError('figi empty')
        interval = request.query_params.get('interval', None)
        if interval is None:
            raise serializers.ValidationError('interval empty')
        from_ = request.query_params.get('from', None)
        if from_ is None:
            raise serializers.ValidationError('from empty')
        to = request.query_params.get('to', None)
        if to is None:
            raise serializers.ValidationError('to empty')

        candles = (candles
                   .values('time__time')
                   .filter(figi=figi, interval=interval, time__range=[from_, to])
                   .annotate(o=Avg('o'), v=Avg('v')))

        page = self.paginate_queryset(candles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(candles, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
