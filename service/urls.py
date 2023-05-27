from django.urls import include, path

from . import views

app_name = "service"

urlpatterns = [
    path("", views.index, name="index"),  # homepage
    path("add_email", views.add_email, name="add_email"),
    path(r"^i18n/", include("django.conf.urls.i18n")),  # translations helpers
]
