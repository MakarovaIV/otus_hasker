import os
import shutil

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from hasker_app.forms import SignUpForm, CustomUserCreationForm

from hasker_app.models import Question


class IndexView(ListView):
    model = Question
    success_url = reverse_lazy("login")
    template_name = "hasker_app/index.html"


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # login(request, user)

            user.picture_data = form.cleaned_data['picture'].file.read()
            user.save()
            shutil.rmtree('tmp_upload')
            return redirect("login")

    else:
        form = SignUpForm()

    return render(request=request,
                  template_name="hasker_app/signup_form.html",
                  context={"form": form})


def login_handler(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="hasker_app/login.html", context={"login_form": form})


def logout_handler(request):
    if request.session:
        logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request=request, template_name="hasker_app/logout.html")
