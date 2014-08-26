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

    """ This is a hack for doing polymorphism """
    @property
    def maturity(self):
        if hasattr(self, 'cashrate'):
            return self.cashrate.maturity()
        if hasattr(self, 'swaprate'):
            return self.swaprate.maturity()

class CashRate(Pillar):
    months = models.IntegerField()
    
    def maturity(self):
        return "%dM" % self.months

    def __unicode__(self):
        return "%s %s CASH" % (self.yield_curve.currency, self.maturity)
    
class SwapRate(Pillar):
    years = models.IntegerField()
    
    def maturity(self):
        return "%dY" % self.years

    def __unicode__(self):
        return "%s %s SWAP" % (self.yield_curve.currency, self.maturity)

