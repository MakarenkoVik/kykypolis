from django.http import JsonResponse
from django.shortcuts import render
from django.db import DatabaseError, IntegrityError
from django.core import mail
from kykypolis import settings
from service.models import Email, Event, Gallery, Review, Service, CallBack


# Getting objects from the database and passing them to the template index.html
def index(request):
    services = Service.objects.filter(is_active=True).order_by("id")
    galleries = Gallery.objects.filter(is_active=True)
    events = Event.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_active=True)
    context = {
        "services": services,
        "galleries": galleries,
        "events": events,
        "reviews": reviews,
    }
    return render(request, "service/index.html", context)


def add_email(request, method=["POST"]):
    email_value = request.POST.get("email")
    if email_value:
        try:
            email_db = Email()
            email_db.email = email_value
            email_db.save()
            return JsonResponse({})
        except DatabaseError as e:
            if "duplicate entry" in str(e).lower():
                return JsonResponse({"duplicate":True})
    raise Exception("Bad data")


def add_phone(request, method=["POST"]):
    name = request.POST.get("firstname")
    phone = request.POST.get("phone")
    if phone:
        phone_db = CallBack()
        phone_db.name = name
        phone_db.phone = phone
        phone_db.save()
        try:
            plain_message = "firstname:{}, phone:{}".format(name, phone)
            mail.send_mail("Call me back please", plain_message, settings.EMAIL_HOST_USER, ["kukupolis@dak.by"])
        except Exception as e:
            print(e)
        return JsonResponse({})
    raise Exception("Bad data")
