from django.db import models
from QuantLib import *

# Create your models here.

class YieldCurve(models.Model):
    name = models.CharField(max_length=30)
    pricing_date = models.DateTimeField()
    currency = models.CharField(max_length=3)

    def __unicode__(self):
        return "%s %s" % (self.name, self.currency)

class Pillar(models.Model):
    yield_curve = models.ForeignKey(YieldCurve)
    rate = models.FloatField()

class CashRate(Pillar):
    months = models.IntegerField()

    def __unicode__(self):
        return "%s %dM CASH" % (self.yield_curve.currency, self.months)
    
class SwapRate(Pillar):
    years = models.IntegerField()

    def __unicode__(self):
        return "%s %dY SWAP" % (self.yield_curve.currency, self.years)
