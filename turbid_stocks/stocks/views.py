from django.db import reset_queries
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
import tinvest
from .models import Token, Instrument
# Create your views here.

TOKEN = Token.objects.get(pk="tinkoff_sandbox").value


def index(request):
    context = {'instrument_count': Instrument.objects.count()}
    return render(request, 'stocks/index.html', context)


def sync(request):
    client = tinvest.SyncClient(TOKEN, use_sandbox=True)
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
