from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import Profile, Dweet
from .forms import DweetForm
from django.contrib.auth.models import User

def SignupPage(request):  # sourcery skip: last-if-guard
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists! Please choose a different one.")

        # If username doesn't exist, create the user
        my_user = User.objects.create_user(uname, password=pass1)
        # Optionally, you can handle additional user setup here
        my_user.save()
        return redirect('dwitter:login')

        



    return render (request,'dwitter/signup.html')

def LoginPage(request):
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('dwitter:dashboard')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'dwitter/login.html')



@login_required(login_url='dwitter:login')
def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user.profile)
        #  profile is an attribute or a related object linked to the User model through a one-to-one relationship.
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

    return render(request, "dwitter/profile.html", {"profile" : profile})

@login_required(login_url='dwitter:login')
def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        dweet = form.save(commit = False)
        dweet.user = request.user
        dweet.save()
        return redirect("dwitter:dashboard")
    
    followed_dweets = Dweet.objects.filter(
        user__profile__in = request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(request, "dwitter/dashboard.html", {"form" : form , "dweets" : followed_dweets})

@login_required(login_url='dwitter:login')
def profile_list(request):
    profiles = Profile.objects.exclude(user = request.user)
    return render(request, "dwitter/profile_list.html", {"profiles" : profiles})

# Create your views here.
