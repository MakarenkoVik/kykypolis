from django.contrib import admin
from service.models import Price, Service
from django.db.models import Avg
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import mark_safe
import io
from django.http import FileResponse
from django.core import serializers
from datetime import datetime

# Register your models here.

class PriceInline(admin.TabularInline):
    model = Price

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = (
        'service',
        'description',
        'value',
        'currency',
        'pub_date',
    )
    list_filter = ('service',)
    search_fields = ('service__name', 'value', 'description',)
    actions = ('make_inactive', 'export_as_json', 'make_active',)

    @admin.action(description='Switch to inactive state')
    def make_inactive(self, request, queryset): 
        queryset.update(is_active=False)
        
    @admin.action(description='Switch to active state')
    def make_active(self, request, queryset): 
        queryset.update(is_active=True)

    @admin.action(description="Download files")
    def export_as_json(self, request, queryset):
        response = FileResponse(
            io.BytesIO(serializers.serialize("json", queryset).encode("utf-8")), 
            as_attachment=True, filename=f"log-{datetime.now()}.json",
        )
        return response

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = (
        'name',
        'pub_date',
        'view_price_link', 
        'average_price',
        'img_preview',
    )

    @admin.display(description="average value")
    def average_price(self, obj):
        result = Price.objects.filter(service=obj).aggregate(Avg('value'))
        return f'{result["value__avg"]:.2f} BYN'

    @admin.display(description="prices")
    def view_price_link(self, obj):
        count = obj.price_set.count()
        url = (
            reverse("admin:service_price_changelist")
            + "?"
            + urlencode({"service_id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Prices</a>', url, count)
    
    search_fields = ('name',)
    inlines = [
        PriceInline, 
    ]
    readonly_fields = ("img_tag",)
    actions = ('make_inactive', 'export_as_json', 'make_active',)

    @admin.display(description='service image')
    def img_preview(self, obj):
        return mark_safe(
            f'<img src = "{obj.service_image.url}" width ="150px" height="150px"/>'
        )
    
    @admin.display(description='service image')
    def img_tag(self, obj): 
        return mark_safe(
            f'<img src = "{obj.service_image.url}" width = "150" height="150px"/>'
        )

    @admin.action(description='Switch to inactive state')
    def make_inactive(self, request, queryset): 
        queryset.update(is_active=False)
        
    @admin.action(description='Switch to active state')
    def make_active(self, request, queryset): 
        queryset.update(is_active=True)

    @admin.action(description="Download files")
    def export_as_json(self, request, queryset):
        response = FileResponse(
            io.BytesIO(serializers.serialize("json", queryset).encode("utf-8")), 
            as_attachment=True, filename=f"log-{datetime.now()}.json",
        )
        return response
    
