from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import CustomUserCreationForm

# Create your views here.

# def index(request):
#     return redirect("/users/login")

# def password_change_done(request):
#     return redirect("/users/login")


def register(request):
    if request.method == "GET":
        return render(request, "registration/register.html", {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("service:index"))
        return render(
            request,
            "registration/register.html",
            {"form": CustomUserCreationForm, "error_message": form.error_messages},
        )
