# dwitter/views.py
# dwitter/views.py
from django.shortcuts import render, redirect
from .forms import DweetForm
from .models import Dweet, Profile
from django.contrib.auth import authenticate,login 
# from django.contrib.auth import authenticate
from django.urls import reverse
from dwitter.forms import CustomUserCreationForm
def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))

def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dashboard")
    followed_dweets = Dweet.objects.filter(
    user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")
    return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "dweets": followed_dweets},
    )


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def password_change(request):
    
    return render(request, "dwitter/registration/password_change_form.html")


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
            current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})


