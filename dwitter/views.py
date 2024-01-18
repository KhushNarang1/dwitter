from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Profile, Dweet
from .forms import DweetForm, SearchForm
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
def delete_dweet(request, dweet_id):
    dweet = get_object_or_404(Dweet, pk=dweet_id)
    if request.user != dweet.user:
        # If not the owner, you may choose to redirect or show an error message
        return HttpResponseRedirect('/error-page')  # Redirect to an error page
    else:
        dweet.delete()
    # print(request.user.id)
    return redirect('dwitter:profile', pk=request.user.pk)


@login_required(login_url='dwitter:login')
def edit_dweet(request, dweet_id):
    dweet = get_object_or_404(Dweet, pk=dweet_id)
    
    # Checking if the logged-in user is the owner of the dweet
    if request.user != dweet.user:
        # If not the owner, you may choose to redirect or show an error message
        return HttpResponseRedirect('/error-page')  # Redirect to an error page
    
    if request.method == 'POST':
        form = DweetForm(request.POST, instance=dweet)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/profile/{request.user.pk}/')
    else:
        form = DweetForm(instance=dweet)
    
    return render(request, 'dwitter/edit_dweet.html', {'form': form})


@login_required(login_url='dwitter:login')
def profile(request, pk):
    print(pk, request.user.pk)
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

    
    
    my_dweets = Dweet.objects.filter(
        user = profile.user
    ).order_by("-created_at")

    return render(request, "dwitter/profile.html", {"profile" : profile, "dweets" : my_dweets})

@login_required(login_url='dwitter:login')
def dashboard(request):  # sourcery skip: use-named-expression
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
def profile_list(request):  # sourcery skip: use-named-expression
    profiles = Profile.objects.all()

    search_query = request.GET.get('search_query')
    if search_query:
        profiles = profiles.filter(user__username__icontains=search_query)

    context = {
        'profiles': profiles,
        'search_form': SearchForm(),
    }
    
    return render(request, "dwitter/profile_list.html", context)


@login_required(login_url='dwitter:login')
def dweet_discription(request, dweet_id):
    dweet = get_object_or_404(Dweet, pk=dweet_id)
    context = {
        'dweet' : dweet,
    }
    return render(request, "dwitter/dweet_discription.html", context)
# Create your views here.

def like_post(request, dweet_id):
    dweet = get_object_or_404(Dweet, id = request.POST.get('post_id'))
    dweet.likes.add(request.user)
    return HttpResponseRedirect(reverse('dwitter:dweet_discription', kwargs = {'dweet_id' : dweet_id}))
