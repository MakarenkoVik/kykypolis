from django.shortcuts import render
from service.models import Service, Price, Gallery, Event, Review
from datetime import datetime


# Create your views here.

def index(request):
    services = Service.objects.filter(is_active = True).order_by('id')
    galleries = Gallery.objects.filter(is_active = True)
    events = Event.objects.filter(is_active = True)
    reviews = Review.objects.filter(is_active = True)
    context = {
        'services': services,
        'galleries': galleries,
        'events': events,
        'reviews': reviews,
    }
    return render(request, "service/index.html", context)


