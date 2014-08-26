from yc.models import YieldCurve, CashRate, SwapRate
from django.contrib import admin

class CashInline(admin.TabularInline):
    model = CashRate
    extra = 1

class SwapInline(admin.TabularInline):
    model = SwapRate
    extra = 1

class YCAdmin(admin.ModelAdmin):
    fields = ['name', 'currency', 'pricing_date']
    inlines = [CashInline, SwapInline]
    list_display = ['name','currency', 'pricing_date']
    
admin.site.register(YieldCurve, YCAdmin)
#admin.site.register(CashRate)
#admin.site.register(SwapRate)
