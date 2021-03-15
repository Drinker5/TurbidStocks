from django.db import reset_queries
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.db.models import Avg, Max, Min, Sum
import tinvest
from .models import Token, Instrument, Candle
from datetime import datetime, timedelta
# Create your views here.


def get_client() -> tinvest.SyncClient:
    token = Token.objects.get(pk="tinkoff").value
    return tinvest.SyncClient(token, use_sandbox=True)


def index(request):
    context = {'instrument_count': Instrument.objects.count()}
    return render(request, 'stocks/index.html', context)


def sync(request):
    client = get_client()
    response = client.get_market_stocks()
    instruments = list(map(lambda i: Instrument(
        figi=i.figi,
        ticker=i.ticker,
        name=i.name,
        currency=i.currency,
        lot=i.lot,
        isin=i.isin),
        response.payload.instruments))
    Instrument.objects.bulk_create(instruments, ignore_conflicts=True)

    fields = request.POST['fields']
    if fields:
        Instrument.objects.bulk_update(instruments, fields=fields.split(','))

    return HttpResponseRedirect(reverse('stocks:index'))


def sync_candles(figi, from_, to, interval):
    candles = Candle.objects.filter(figi=figi, interval=interval)
    aggr = candles.aggregate(min=Min('time'), max=Max('time'))
    minTime = aggr['min']
    maxTime = aggr['max']

    if minTime is None and maxTime is None:
        load_candles(figi, from_, to, interval)
    else:
        minTime = convert_time(minTime, interval, -1)
        maxTime = convert_time(minTime, interval)
        if from_ < minTime:
            load_candles(figi, from_, minTime, interval)
        if to > maxTime:
            load_candles(figi, maxTime, to, interval)


def convert_time(time: datetime, interval: str, way=1):
    tinterval = tinvest.CandleResolution[interval]
    delta = timedelta(0)
    if tinterval == tinvest.CandleResolution.min1:
        delta = timedelta(min=1)
    if tinterval == tinvest.CandleResolution.min2:
        delta = timedelta(min=2)
    if tinterval == tinvest.CandleResolution.min3:
        delta = timedelta(min=3)
    if tinterval == tinvest.CandleResolution.min5:
        delta = timedelta(min=5)
    if tinterval == tinvest.CandleResolution.min10:
        delta = timedelta(min=10)
    if tinterval == tinvest.CandleResolution.min15:
        delta = timedelta(min=15)
    if tinterval == tinvest.CandleResolution.min30:
        delta = timedelta(min=30)
    if tinterval == tinvest.CandleResolution.hour:
        delta = timedelta(hours=1)
    if tinterval == tinvest.CandleResolution.day:
        delta = timedelta(days=1)
    if tinterval == tinvest.CandleResolution.week:
        delta = timedelta(days=7)
    if tinterval == tinvest.CandleResolution.month:
        delta = timedelta(days=30)

    return time + way * delta


def load_candles(figi, from_, to, interval):
    if from_ == to:
        return

    client = get_client()
    response = client.get_market_candles(
        figi=figi, from_=from_, to=to, interval=tinvest.CandleResolution[interval])
    candles = list(map(lambda i: Candle(
        figi=i.figi,
        o=i.o,
        c=i.c,
        h=i.h,
        l=i.l,
        v=i.v,
        interval=interval,
        time=i.time),
        response.payload.candles))
    candles
    Candle.objects.bulk_create(candles, ignore_conflicts=True)
