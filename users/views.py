from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm

#This class will let us create an authentication form.
from django.contrib.auth.forms import AuthenticationForm
# This function will let us log the user
from django.contrib.auth import login

from django.contrib import messages
from .models import Topics
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            messages.success(request, f"Account created for {username}.")
        return redirect(to="/")
    else:
        form = RegistrationForm()
        return render(request, "users/register.html", {"form":form})

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
            new_topic = None
            # If user has no topics read, just asign the first one.
            if user.profile.topics_read.count() == 0:
                new_topic = Topics.objects.all().first()
                user.profile.topics_read.add(new_topic)
                user.profile.save()
                return redirect(to=f"/topic/{new_topic.pk}/{user.id}")
            # This one is important because if all the topics available have already been read by the user
            # The following else statement will leave the new_topic variable empty.
            elif user.profile.topics_read.count() == Topics.objects.count():
                new_topic = Topics.objects.all().last()
            else:
                # If the topic is not in all the topics, make it the topic of the day
                # and save it to topics read.
                for topic in Topics.objects.all():
                    if topic not in user.profile.topics_read.all():
                        new_topic = topic
                        user.profile.topics_read.add(new_topic)
                        user.profile.save()
                        break
        else:
            # This is important so in case the user types a wrong username or password
            # the page won't crash.
            form = AuthenticationForm()
            messages.error(request, "Incorrect Username or Password.")
            return render(request, "users/login_manual.html", {"form":form})
        return redirect(to=f"/topic/{new_topic.pk}/{user.id}")
    else:
        # If it is a GET request.
        form = AuthenticationForm()
        return render(request, "users/login_manual.html", {"form":form})

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


