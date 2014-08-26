from django.shortcuts import render_to_response

def index(request):
    curves = YieldCurve.objects.all().order_by('-pricing_date')
    return render_to_response('yc/index.html', {'curves': curves})
    #t = loader.get_template('yc/index.html')
    #c = Context({
    #        'curves': curves,
    #        })
    #return HttpResponse(t.render(c))
