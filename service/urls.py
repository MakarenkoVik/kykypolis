from django.urls import include, path

from . import views

app_name = "service"

urlpatterns = [
    path("", views.index, name="index"), # homepage
    path(r"^i18n/", include("django.conf.urls.i18n")), # translations helpers
]
