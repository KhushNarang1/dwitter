from django.shortcuts import render
from .models import Profile

def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
    return render(request, "dwitter/profile.html", {"profile" : profile})

def dashboard(request):
    return render(request, "base.html")

def profile_list(request):
    profiles = Profile.objects.exclude(user = request.user)
    return render(request, "dwitter/profile_list.html", {"profiles" : profiles})

# Create your views here.
