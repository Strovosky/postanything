# Python built-in views
from datetime import date

# Forms
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm

# Manual Login required imports
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login # This function will let us log the user

# Django Views
from django.views.generic import DetailView

# Models
from .models import Topics
from django.contrib.auth.models import User

# Others
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


######################################################################################
# SingUp

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            messages.success(request, f"Account created for {username}.")
        return redirect(to="/login/")
    else:
        form = RegistrationForm()
        return render(request, "users/register.html", {"form":form})


########################################################################################
# LogIn

# We have to create a function view instead of the built-in Login view
# because we want to redirect to a very specifi url with a pk as an argument.
def login_view(request):
    if request.method == "POST":
        # Specifying data= is IMPORTANT here cuz request.POST is not the first paramether for this class.
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # This is how you get the user.
            user = form.get_user()
            # This is how you log the user in.
            login(request, user)
            topic = None
            # Means: If the user has read a topic and the topic isn't today's...
            if user.profile.topics_read.count() == Topics.objects.all().count():
                topic = Topics.objects.get(id=user.profile.topics_read.count())
            elif user.profile.started_reading != None and user.profile.started_reading != date.today():
                # I have to create a time delta to see how many days of difference.
                days_of_difference = date.today() - user.profile.started_reading
                topic = Topics.objects.get(id= 1 + days_of_difference.days)
                #for ind, day in enumerate(range(days_of_difference.days), start=1):
                #    temp_topic = Topics.objects.get(id=ind)
                #    if temp_topic not in user.profile.topics_read:
                #        user.profile.topics_read.add(temp_topic)
                user.profile.topics_read.add(topic)
                user.profile.save()
            else:
                topic = Topics.objects.get(pk=1)
                user.profile.started_reading = date.today()
                user.profile.topics_read.add(topic)
                user.profile.save()
            return redirect(to=f"/topic/{topic.pk}/{user.id}")
        else:
            # This is important so in case the user types a wrong username or password
            # the page won't crash.
            form = AuthenticationForm()
            messages.error(request, "Incorrect Username or Password.")
            return render(request, "users/login_manual.html", {"form":form})
    else:
        # If it is a GET request.
        form = AuthenticationForm()
        return render(request, "users/login_manual.html", {"form":form})


########################################################################################
# Update

@login_required(login_url="/login/")
def update_user(request):
    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, "User info has been updated")
    else:
        user_update_form = UserUpdateForm()
        profile_update_form = ProfileUpdateForm()
    return render(request, "users/update_user.html", {"user_form": user_update_form, "profile_form":profile_update_form})


########################################################################################
# User Profile

class ProfileDetailView(DetailView):
    model = User
    template_name: str = "users/user_profile.html"
