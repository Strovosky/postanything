from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Topics
from django.contrib.auth.decorators import login_required

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


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        print(f"{username}")
        password = request.POST["password"]
        print(f"{password}")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active and user.is_authenticated:
            print("It didn't authenticate the user.")
            login(request, user)
            # If user hasn't read any prior topics, they'll read the first.
            if user.profile.topics_read.count() == 0:
                return redirect(to="{% url 'topic_detail' 1 %}")
            else:
                for topic in Topics.objects.all():
                    if not topic in user.profile.topics_read.all():
                        user.profile.topics_read.add(topic)
                        user.profile.topics_read.save()
                        return redirect(to="{% url 'topic_detail' topic.id %}")
    else:
        print("It was a get.")
        return render(request, "users/login_manual.html")

@login_required
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


