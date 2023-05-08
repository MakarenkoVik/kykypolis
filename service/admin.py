import io
from datetime import datetime

from django.contrib import admin
from django.core import serializers
from django.db.models import Avg
from django.http import FileResponse
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from django.utils.http import urlencode

from service.models import Event, Gallery, Price, Review, Service

# Register your models here.

# Adding a child price model to the parent service on one page.
class PriceInline(admin.TabularInline):
    model = Price


# Register model Price.
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = (
        "service",
        "description",
        "value",
        "currency",
        "pub_date",
    )
    list_filter = ("service",)
    search_fields = (
        "service__name",
        "value",
        "description",
    )
    actions = (
        "make_inactive",
        "export_as_json",
        "make_active",
    )

    # Setting the is_active field to False.
    @admin.action(description="Switch to inactive state")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    # Setting the is_active field to True.
    @admin.action(description="Switch to active state")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    # Dump database as json.
    @admin.action(description="Download files")
    def export_as_json(self, request, queryset):
        response = FileResponse(
            io.BytesIO(serializers.serialize("json", queryset).encode("utf-8")),
            as_attachment=True,
            filename=f"log-{datetime.now()}.json",
        )
        return response


# Register model Service.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = (
        "name",
        "pub_date",
        "view_price_link",
        "average_price",
        "img_preview",
    )

    # Average service price.
    @admin.display(description="average value")
    def average_price(self, obj):
        if Price.objects.filter(service=obj):
            result = Price.objects.filter(service=obj).aggregate(Avg("value"))
            return f'{result["value__avg"]:.2f} BYN'
        else:
            None

    # Link to the prices of a specific service.
    @admin.display(description="prices")
    def view_price_link(self, obj):
        count = obj.price_set.count()
        url = reverse("admin:service_price_changelist") + "?" + urlencode({"service_id": f"{obj.id}"})
        return format_html('<a href="{}">{} Prices</a>', url, count)

    search_fields = ("name",)
    inlines = [
        PriceInline,
    ]
    readonly_fields = ("img_tag",)
    actions = (
        "make_inactive",
        "export_as_json",
        "make_active",
    )

    # Preview in the list of objects.
    @admin.display(description="service image")
    def img_preview(self, obj):
        return mark_safe(f'<img src = "{obj.service_image.url}" width ="200px" height="150px"/>')
    
    # Preview on change view page.
    @admin.display(description="service image")
    def img_tag(self, obj):
        return mark_safe(f'<img src = "{obj.service_image.url}" width = "200" height="150px"/>')
    
    # Setting the is_active field to False.
    @admin.action(description="Switch to inactive state")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    # Setting the is_active field to True.
    @admin.action(description="Switch to active state")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    # Dump database as json.
    @admin.action(description="Download files")
    def export_as_json(self, request, queryset):
        response = FileResponse(
            io.BytesIO(serializers.serialize("json", queryset).encode("utf-8")),
            as_attachment=True,
            filename=f"log-{datetime.now()}.json",
        )
        return response


# Register model Gallery.
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = (
        "photographer",
        "pub_date",
        "place",
        "img_preview",
    )
    actions = ("make_inactive", "make_active")
    readonly_fields = ("img_tag",)
    search_fields = (
        "photographer",
        "place",
    )

    # Setting the is_active field to False.
    @admin.action(description="Switch to inactive state")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    # Setting the is_active field to True.
    @admin.action(description="Switch to active state")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    # Preview in the list of objects.
    @admin.display(description="gallery image")
    def img_preview(self, obj):
        return mark_safe(f'<img src = "{obj.gallery_image_small.url}" width ="150px" height="150px"/>')
    
    # Preview on change view page.
    @admin.display(description="gallery image")
    def img_tag(self, obj):
        return mark_safe(f'<img src = "{obj.gallery_image_small.url}" width = "150" height="150px"/>')


# Register model Event.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = (
        "name",
        "date",
        "description",
        "img_preview",
    )

    search_fields = (
        "name",
        "date",
        "description",
    )
    readonly_fields = ("img_tag",)
    actions = (
        "make_inactive",
        "export_as_json",
        "make_active",
    )

    # Preview in the list of objects.
    @admin.display(description="event image")
    def img_preview(self, obj):
        return mark_safe(f'<img src = "{obj.event_image.url}" width ="150px" height="150px"/>')
    
    # Preview on change view page.
    @admin.display(description="event image")
    def img_tag(self, obj):
        return mark_safe(f'<img src = "{obj.event_image.url}" width = "150" height="150px"/>')
    
    # Setting the is_active field to False.
    @admin.action(description="Switch to inactive state")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    
    # Setting the is_active field to True.
    @admin.action(description="Switch to active state")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    
    # Dump database as json.
    @admin.action(description="Download files")
    def export_as_json(self, request, queryset):
        response = FileResponse(
            io.BytesIO(serializers.serialize("json", queryset).encode("utf-8")),
            as_attachment=True,
            filename=f"log-{datetime.now()}.json",
        )
        return response


# Register model Review.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = (
        "visitor_name",
        "visitor_category",
        "description",
        "link",
        "img_preview",
        "pub_date",
    )

    search_fields = (
        "visitor_name",
        "visitor_category",
        "description",
    )
    readonly_fields = ("img_tag",)
    actions = (
        "make_inactive",
        "export_as_json",
        "make_active",
    )
    
    # Preview in the list of objects.
    @admin.display(description="review image")
    def img_preview(self, obj):
        return mark_safe(f'<img src = "{obj.review_image.url}" width ="150px" height="150px"/>')
    
    # Preview on change view page.
    @admin.display(description="review image")
    def img_tag(self, obj):
        return mark_safe(f'<img src = "{obj.review_image.url}" width = "150" height="150px"/>')
    
    # Setting the is_active field to False.
    @admin.action(description="Switch to inactive state")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    
    # Setting the is_active field to True.
    @admin.action(description="Switch to active state")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    
    # Dump database as json.
    @admin.action(description="Download files")
    def export_as_json(self, request, queryset):
        response = FileResponse(
            io.BytesIO(serializers.serialize("json", queryset).encode("utf-8")),
            as_attachment=True,
            filename=f"log-{datetime.now()}.json",
        )
        return response
