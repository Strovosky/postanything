from django.db.models import Model, CharField, IntegerField, DateTimeField, ForeignKey, CASCADE
from django.contrib.auth.models import User


# This model will handle the topic people will discuss.
class Topics(Model):
    content = CharField(max_length=250)
    num_likes = IntegerField(default=0)

    def __str__(self) -> str:
        return self.content

#########################################################

# This model will handle the comments on the topics
class Comments(Model):
    content = CharField(max_length=300)
    num_likes = IntegerField(default=0)
    date_created = DateTimeField(auto_now=True)
    author = ForeignKey(to=User, on_delete=CASCADE)
    topic = ForeignKey(to=Topics, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.date_created}"

#########################################################

# This model will handle the subcomments made about the comments
class Subcomments(Model):
    content = CharField(max_length=300)
    num_likes = IntegerField(default=0)
    date_created = DateTimeField(auto_now=True)
    author = ForeignKey(to=User, on_delete=CASCADE)
    parent_comment = ForeignKey(to=Comments, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.content}"
