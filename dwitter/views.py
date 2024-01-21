from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

from .models import Profile, Dweet
from .forms import DweetForm, SearchForm, CommentForm, SignUpForm, SignInForm
from django.contrib.auth.models import User



def SignupPage(request):  # sourcery skip: extract-method, remove-unreachable-code
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['name']
            if User.objects.filter(username=username).exists():
                return render(request, 'dwitter/signup.html', {'form': form, 'error_message': 'Username already exists. Please choose a different one.'})

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, first_name = first_name, password=password)
            user.save()
            return redirect('dwitter:login')

    else:
        form = SignUpForm()

    return render(request, 'dwitter/signup.html', {'form': form})


# def LoginPage(request):
#     # sourcery skip: remove-unnecessary-else, swap-if-else-branches
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('dwitter:dashboard')
#         else:
#             return HttpResponse ("Username or Password is incorrect!!!")

#     return render (request,'dwitter/login.html')

def LoginPage(request):
    # sourcery skip: extract-method, remove-unnecessary-else, swap-if-else-branches
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user using email and password
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # User is authenticated, log them in
                login(request, user)
                return redirect('dwitter:dashboard')  # Replace 'dashboard' with your actual dashboard URL
            else:
                # User is not authenticated, show an error message
                return render(request, 'dwitter/login.html', {'form': form, 'error_message': 'Invalid email or password.'})
    else:
        form = SignInForm()

    return render(request, 'dwitter/login.html', {'form': form})

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
            return redirect(f'/profile/{request.user.pk}/')
    else:
        form = DweetForm(instance=dweet)
    
    return render(request, 'dwitter/edit_dweet.html', {'form': form})


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

    
    
    my_dweets = Dweet.objects.filter(
        user = profile.user
    ).order_by("-created_at")

    return render(request, "dwitter/profile.html", {"profile" : profile, "dweets" : my_dweets})

@login_required(login_url='dwitter:login')
def dashboard(request):  # sourcery skip: use-named-expression
    form = DweetForm(request.POST or None,request.FILES or None)
    if(request.method=='POST'):
        print(request.POST,request.FILES)
    if request.method == "POST" and form.is_valid():
        # if(request.FILES!=None)/
        dweet = form.save(commit = False)
        # print(dweet)
        dweet.user = request.user
        dweet.save()
        form.save_m2m()
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
    form = CommentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            comment = form.save(commit=False)
            comment.user = request.user
            comment.dweet = dweet  # Associate the comment with the specific dweet
            comment.save()
            return redirect('dwitter:dweet_discription', dweet_id=dweet_id)
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            # Handle the error, such as displaying an error message to the user

    context = {'dweet': dweet, 'form': form}
    return render(request, "dwitter/dweet_discription.html", context)
# Create your views here.

def like_post(request, dweet_id):
    dweet = get_object_or_404(Dweet, id=request.POST.get('post_id'))

    if request.user in dweet.likes.all():
        dweet.likes.remove(request.user)
    else:
        dweet.likes.add(request.user)

    return redirect('dwitter:dweet_discription', dweet_id=dweet_id)


