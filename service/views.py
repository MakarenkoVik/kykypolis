from django.shortcuts import render
from service.models import Service, Price
from datetime import datetime


# Create your views here.

def index(request):
    services = Service.objects.filter(is_active = True)
    return render(request, 'service/index.html', {'service': services})


