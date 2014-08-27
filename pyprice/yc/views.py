from django.shortcuts import render_to_response, get_object_or_404
from yc.models import YieldCurve
#from QuantLib import PiecewiseFlatForward, Actual360, Days, TARGET, Date, Compoounded
from QuantLib import *
from django.http import HttpResponse


def index(request):
    curves = YieldCurve.objects.all().order_by('-pricing_date')
    return render_to_response('yc/index.html', {'curves': curves})
    #t = loader.get_template('yc/index.html')
    #c = Context({
    #        'curves': curves,
    #        })
    #return HttpResponse(t.render(c))

def curve(request, curve_id):
    curve = get_object_or_404(YieldCurve, pk=curve_id)
    pillars = curve.pillar_set.all()

    return render_to_response('yc/curve.html', {'curve': curve, 'pillars': pillars})

def curve_data(request, curve_id):
    curve = get_object_or_404(YieldCurve, pk=curve_id)
    pillars = curve.pillar_set.all()
    calendar = TARGET()
    today = calendar.adjust(Date(curve.pricing_date.day, curve.pricing_date.month, curve.pricing_date.year))
    settlement = calendar.advance(today,curve.settlement_days,Days)
    termstructure = PiecewiseFlatForward(settlement,
                                         [x.QLpillar() for x in pillars],
                                         Actual360()
                                         )

    max_time = termstructure.maxTime()
    zeros = [ (max_time * x / 250.0, termstructure.zeroRate(max_time * x / 250.0, Compounded).rate()) for x in range(0, 250) ]
    s = "time,rate,type\n"
    for zero in zeros:
        s = s + "%f, %f,0\n" % zero
    for forward in termstructure.nodes():
        zero = termstructure.zeroRate((forward[0] - today) / 365.0, Compounded).rate()
        s = s + "%f, %f,1\n" % ((forward[0] - today) / 365.0, zero)

    return HttpResponse(s, content_type = "text/csv")
