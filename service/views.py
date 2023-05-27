from django.shortcuts import render
from django.http import JsonResponse
from service.models import Event, Gallery, Review, Service, Email


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


def add_email(request, method=['POST']):
    email_value = request.POST.get('email')
    if email_value:
        email_db = Email()
        email_db.email = email_value
        email_db.save()
        return JsonResponse({})
    raise Exception("Bad data")
