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
    list_filter = ['currency', 'pricing_date']
    search_fields = ['name']
    date_hierarchy = 'pricing_date'
    save_as = True

admin.site.register(YieldCurve, YCAdmin)
