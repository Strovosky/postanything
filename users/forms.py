from django.forms import EmailField, CharField, ImageField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = EmailField()
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


###############################################################

# The user fields I want the user to be able to update.
class UserUpdateForm(ModelForm):
    email = EmailField(label="Update Email", required=False)
    class Meta:
        model = User
        fields = ["email"]

###############################################################

# The profile fields I want the user to be able to update.
class ProfileUpdateForm(ModelForm):
    profile_pic = ImageField(required=False, label="Update Profile Picture")
    about_me = CharField(required=False, label="Update About Me")
    class Meta:
        model = Profile
        fields = ["profile_pic", "about_me"]
