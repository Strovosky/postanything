from email.mime import image
from django.db.models import Model, ImageField, CharField, ManyToManyField, OneToOneField, DateField, CASCADE
from django.contrib.auth.models import User
from blog.models import Topics
from PIL import Image

# Create your models here.

class Profile(Model):

    # One user can have exclusively one profile.
    user = OneToOneField(to=User, on_delete=CASCADE)
    profile_pic = ImageField(default='default_pic.png', upload_to='profile_pics/')
    
    about_me = CharField(max_length=200, blank=True, null=True)
    
    # One user can read many topics and one topic can be read by many users.
    # It's set to deault=None because when created they haven't read any topics.
    # Once they go to a topic page for the first time, topics_read will be added.
    topics_read = ManyToManyField(to=Topics, default=None, blank=True)

    # This field will set the day when they started reading the first topic.
    started_reading = DateField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return f"Profile: {self.user}"
    
    # To resize the imgage if it is too big
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
