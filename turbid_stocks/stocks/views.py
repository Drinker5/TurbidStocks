from django.db import reset_queries
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.db.models import Avg, Max, Min, Sum
import tinvest
from .models import Token, Instrument, Candle
from datetime import datetime, timedelta
from tenacity import retry, retry_if_exception_type, wait_fixed, before, before_log
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

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
        minTime = minTime - get_delta_by_interval(interval)
        maxTime = maxTime + get_delta_by_interval(interval)
        if from_ < minTime:
            load_candles(figi, from_, minTime, interval)
        if to > maxTime:
            load_candles(figi, maxTime, to, interval)


def get_delta_by_interval(interval: str):
    tinterval = interval_from_str(interval)
    if tinterval == tinvest.CandleResolution.min1:
        return timedelta(minutes=1)
    if tinterval == tinvest.CandleResolution.min2:
        return timedelta(minutes=2)
    if tinterval == tinvest.CandleResolution.min3:
        return timedelta(minutes=3)
    if tinterval == tinvest.CandleResolution.min5:
        return timedelta(minutes=5)
    if tinterval == tinvest.CandleResolution.min10:
        return timedelta(minutes=10)
    if tinterval == tinvest.CandleResolution.min15:
        return timedelta(minutes=15)
    if tinterval == tinvest.CandleResolution.min30:
        return timedelta(minutes=30)
    if tinterval == tinvest.CandleResolution.hour:
        return timedelta(hours=1)
    if tinterval == tinvest.CandleResolution.day:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.week:
        return timedelta(days=7)
    if tinterval == tinvest.CandleResolution.month:
        return timedelta(days=30)

    return timedelta(0)


"""
Интервал свечи и допустимый промежуток запроса:
 1min [ 1 minute,  1 day  ]
 2min [ 2 minutes, 1 day  ]
 3min [ 3 minutes, 1 day  ]
 5min [ 5 minutes, 1 day  ]
10min [10 minutes, 1 day  ]
15min [15 minutes, 1 day  ]
30min [30 minutes, 1 day  ]
 hour [ 1 hour,    7 days ]
  day [ 1 day,     1 year ]
 week [ 7 days,    2 years]
month [ 1 month,  10 years]
"""


def max_allowed_request_interval(interval: str):
    tinterval = interval_from_str(interval)
    if tinterval == tinvest.CandleResolution.min1:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.min2:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.min3:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.min5:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.min10:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.min15:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.min30:
        return timedelta(days=1)
    if tinterval == tinvest.CandleResolution.hour:
        return timedelta(days=7)
    if tinterval == tinvest.CandleResolution.day:
        return timedelta(days=365)
    if tinterval == tinvest.CandleResolution.week:
        return timedelta(days=365*2)
    if tinterval == tinvest.CandleResolution.month:
        return timedelta(days=365*10)

    return timedelta(days=1)


def interval_from_str(value: str) -> tinvest.CandleResolution:
    if value == "1min":
        return tinvest.CandleResolution.min1
    if value == "2min":
        return tinvest.CandleResolution.min2
    if value == "3min":
        return tinvest.CandleResolution.min3
    if value == "5min":
        return tinvest.CandleResolution.min5
    if value == "10min":
        return tinvest.CandleResolution.min10
    if value == "15min":
        return tinvest.CandleResolution.min15
    if value == "30min":
        return tinvest.CandleResolution.min30
    return tinvest.CandleResolution[value]


def load_candles(figi, from_, to, interval):
    if from_ == to:
        return

    # Проверка максимально допустимого промежутка для загрузки свечей
    max_delta = max_allowed_request_interval(interval)
    delta = get_delta_by_interval(interval)
    tinterval = interval_from_str(interval)

    from_i = from_
    to_i = from_i + max_delta
    if to_i > to:
        to_i = to
    while from_i < to:
        # Проверка минимального допустимого промежутка для загрузки свечей
        if to_i - from_i < delta:
            break
        load_candles_internal(figi, from_i, to_i, interval, tinterval)

        from_i = from_i + max_delta
        to_i = to_i + max_delta
        if to_i > to:
            to_i = to


@retry(wait=wait_fixed(60),
       retry=retry_if_exception_type(tinvest.TooManyRequestsError),
       before=before_log(logger, logging.DEBUG))
def load_candles_internal(figi, from_i, to_i, interval, tinterval):
    client = get_client()
    response = client.get_market_candles(
        figi=figi, from_=from_i, to=to_i, interval=tinterval)
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
    Candle.objects.bulk_create(candles, ignore_conflicts=True)
