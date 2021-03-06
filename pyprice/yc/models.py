from django.db import models
from QuantLib import *

# Create your models here.

class YieldCurve(models.Model):
    name = models.CharField(max_length=30)
    pricing_date = models.DateTimeField()
    currency = models.CharField(max_length=3)
    
    # TODO: this hasn't been configured in admin 
    settlement_days = models.IntegerField(default=2)

    def __unicode__(self):
        return "%s %s" % (self.name, self.currency)

    @property
    def date(self):
        return self.pricing_date.strftime("%d %b, %Y")

class Pillar(models.Model):
    yield_curve = models.ForeignKey(YieldCurve)
    rate = models.FloatField()

    """ This is a hack for doing polymorphism """
    def get_child(self):
        if hasattr(self, 'cashrate'):
            return self.cashrate
        if hasattr(self, 'swaprate'):
            return self.swaprate

    @property
    def maturity(self):
        return self.get_child().maturity()

    @property
    def type(self):
        return self.get_child().type()

    def QLpillar(self):
        return self.get_child().QLpillar()

class CashRate(Pillar):
    months = models.IntegerField()
    
    def type(self):
        return "CASH"

    def maturity(self):
        return "%dM" % self.months

    def QLpillar(self):
        return DepositRateHelper(
            QuoteHandle(SimpleQuote(self.rate/100)),
            Period(self.months, Months),
            self.yield_curve.settlement_days,
            TARGET(),
            ModifiedFollowing,
            False,
            Actual360()
            )


    def __unicode__(self):
        return "%s %s CASH" % (self.yield_curve.currency, self.maturity())
    
class SwapRate(Pillar):
    years = models.IntegerField()
    
    def type(self):
        return "SWAP"

    def maturity(self):
        return "%dY" % self.years

    def QLpillar(self):
        return SwapRateHelper(
                QuoteHandle(SimpleQuote(self.rate/100)),
                Period(self.years, Years),
                TARGET(),
                Annual,
                Unadjusted,
                Thirty360(),
                Euribor6M()
                )

    def __unicode__(self):
        return "%s %s SWAP" % (self.yield_curve.currency, self.maturity())


class FRA(Pillar):
    expiry = models.IntegerField()
    tenor = models.IntegerField()

    def type(self):
        return "FRA"

    def maturity(self):
        return "%dM in %dM" % (self.tenor, self.maturity)

    def QLpillar(self):
        return FraRateHelper(QuoteHandle(SimpleQuote(self.rate)),
                             self.maturity, self.tenor,
                             self.yield_curve.settlement_days,
                             TARGET(),
                             ModifiedFollowing,
                             False,
                             Actual360())

    def __unicode__(self):
        return "%s %s FRA" % (self.yield_curve.currency, self.maturity())

class FuturesRate(Pillar):
    expiry = models.DateField()
    tenor = models.IntegerField(default = 3)

    def type(self):
        return "Futures"

    def maturity(self):
        return "%s" % (self.expiry.strptime("%Y-%m-%d"))

    def QLpillar(self):
        return FuturesRateHelper(QuoteHandle(SimpleQuote(self.rate)),
                                 self.expiry, self.tenor,
                                 TARGET(), ModifiedFollowing,
                                 True, Actual360(),
                                 QuoteHandle(SimpleQuote(0.0)))

    def __unicode__(self):
        return "%s %s Futures" % (self.yield_curve.currency, self.maturity())

