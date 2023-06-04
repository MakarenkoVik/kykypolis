from django.urls import include, path

from . import views

app_name = "service"

urlpatterns = [
    path("", views.index, name="index"),  # homepage
    path("add_email", views.add_email, name="add_email"),
    path("add_phone", views.add_phone, name="add_phone"),
    path(r"^i18n/", include("django.conf.urls.i18n")),  # translations helpers
]
