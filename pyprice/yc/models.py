from django.db import models
from QuantLib import *

# Create your models here.

class YieldCurve(models.Model):
    pricing_date = models.DateTimeField()
    currency = models.CharField(max_length=3)

class Pillar(models.Model):
    yield_curve = models.ForeignKey(YieldCurve)
    rate = models.FloatField()

class CashRate(Pillar):
    months = models.IntegerField()
    
class SwapRate(Pillar):
    years = models.IntegerField()
