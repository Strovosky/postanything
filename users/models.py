from django.db.models import Model, ImageField, CharField, ManyToManyField, OneToOneField, DateField, CASCADE
from django.contrib.auth.models import User
from blog.models import Topics

# Create your models here.

class Profile(Model):

    # One user can have exclusively one profile.
    user = OneToOneField(to=User, on_delete=CASCADE)
    profile_pic = ImageField(default='default_pic.jpg', upload_to='profile_pics/')
    #ENGLISH_LEVEL = (
    #    ("Basic", "Basic"),
    #    ("Intermediate", "Intermadiate"),
    #    ("Advanced", "Advanced")
    #)
    about_me = CharField(max_length=200, blank=True, null=True)
    #PROGRESS = (
    #    ("Baby", "Baby"),
    #    ("Kid", "Kid"),
    #    ("Teen", "Teen"),
    #    ("Adult", "Adult"),
    #    ("Expert", "Expert"),
    #    ("Master", "Master")
    #)
    # One user can read many topics and one topic can be read by many users.
    # It's set to deault=None because when created they haven't read any topics.
    # Once they've been created, I use topics_read.add
    topics_read = ManyToManyField(to=Topics, default=None, blank=True)

    # This field will set the day when they started reading the first topic.    
    started_reading = DateField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return f"Profile: {self.user}"
