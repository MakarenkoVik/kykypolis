import io
from datetime import datetime

from django.contrib import admin
from django.core import mail, serializers
from django.db.models import Avg
from django.http import FileResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html, mark_safe, strip_tags
from django.utils.http import urlencode

from kykypolis import settings
from service.models import Email, Event, Gallery, Price, Review, Service, CallBack


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
        "is_access",
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
    actions = ("make_inactive", "make_active", "fill_place", "fill_photographer")
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

    # Filling in the fields place and place_en.
    @admin.action(description="Fill in the place and place_en fields")
    def fill_place(self, request, queryset):
        queryset.update(
            place="хутор Лизаветин, Дзержинский район, Минская область, Беларусь",
            place_en="farm Lizavetin, Dzerzhinsky district, Minsk region, Belarus",
        )

    # Filling in the fields photographer and photographer_en.
    @admin.action(description="Fill in the photographer and photographer_en fields")
    def fill_photographer(self, request, queryset):
        queryset.update(photographer="Кукуполис", photographer_en="Kukupolis")

    # Preview in the list of objects.
    @admin.display(description="gallery image")
    def img_preview(self, obj):
        if obj.gallery_image_small:
            return mark_safe(f'<img src = "{obj.gallery_image_small.url}" width ="200px" height="150px"/>')
        return None

    # Preview on change view page.
    @admin.display(description="gallery image")
    def img_tag(self, obj):
        if obj.gallery_image_small:
            return mark_safe(f'<img src = "{obj.gallery_image_small.url}" width = "150" height="150px"/>')
        return None


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
        "send_emails",
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

    @admin.action(description="Send email with selected events to users")
    def send_emails(self, request, queryset):
        subject = "Hello a new event is here!"
        html_message = render_to_string("service/email.html", {"events": queryset})
        plain_message = strip_tags(html_message)
        for it in Email.objects.filter(is_active=True):
            mail.send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [it.email], html_message=html_message)

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
        if obj.review_image:
            return mark_safe(f'<img src = "{obj.review_image.url}" width ="150px" height="150px"/>')
        return mark_safe(f'<img src = "" width ="150px" height="150px"/>')

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


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = (
        "email",
        "pub_date",
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


@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = (
        "name",
        "phone",
        "pub_date",
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
