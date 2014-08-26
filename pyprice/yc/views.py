from django.shortcuts import render_to_response, get_object_or_404
from yc.models import YieldCurve

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

    termstructure = PiecewiseFlatForward(settlement,
                                         [x.QLpillar() for x in pillars],
                                         Actual360()
                                         )

    return render_to_response('yc/curve.html', {'curve': curve, 'pillars': pillars})
