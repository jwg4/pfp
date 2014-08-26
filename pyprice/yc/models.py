from django.db import models
from QuantLib import *

# Create your models here.

class YieldCurve(models.Model):
    name = models.CharField(max_length=30)
    pricing_date = models.DateTimeField()
    currency = models.CharField(max_length=3)

    def __unicode__(self):
        return "%s %s" % (name, currency)

class Pillar(models.Model):
    yield_curve = models.ForeignKey(YieldCurve)
    rate = models.FloatField()

class CashRate(Pillar):
    months = models.IntegerField()

    def __unicode__(self):
        return "%s %dM CASH" % (yield_curve.currency, months)
    
class SwapRate(Pillar):
    years = models.IntegerField()

    def __unicode__(self):
        return "%s %dY SWAP" % (yield_curve.currency, years)
