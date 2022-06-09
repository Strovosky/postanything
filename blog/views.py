from urllib import response
from django.shortcuts import render

# For Class-based Views
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from .models import Subcomments, Topics, Comments
from django.contrib.auth.models import User

# Forms
from .forms import NewComment, NewSubcomment

# Alerts
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'blog/index.html')


###################################################################
# Topic Views

# We will use a function view instead of a class view cuz we neeed the view to handle GET and POST 
# requests since we'll be creating comments.
@login_required(login_url="login/")
def topic_detail_view(request, pk, user_id):
    if request.method == "POST":
        form = NewComment(request.POST)
        topic = Topics.objects.get(pk=pk)
        user = User.objects.get(id=user_id)
        topic_comments = Comments.objects.filter(topic=topic)
        subcomments = Subcomments.objects.all()

        # If a subcomment was created
        for comment in topic.comments_set.all():
            if request.POST.get("btn_subcomment") == str(comment.id):
                content = request.POST.get("txt_subcomment")
                subcomment = Subcomments.objects.create(content=content, author=user, parent_comment=comment)
                subcomment.save()

        # If a comment was created
        if form.is_valid():
            Comments.objects.create(content=form.cleaned_data["comment"], author=user, topic=topic)
            messages.success(request, "Comment created")
        return render(request, "blog/topic.html", {"form":form, "topic_comments":topic_comments, "topic":topic, "subcomments":subcomments})
    else:
        form = NewComment()
        topic = Topics.objects.get(pk=pk)
        topic_comments = Comments.objects.filter(topic=topic)
        return render(request, "blog/topic.html", {"form":form, "topic":topic, "topic_comments":topic_comments})

#class TopicDetailView(LoginRequiredMixin, DetailView):
#    model = Topics
#    template_name: str = "blog/topic.html"

#@login_required(login_url="login/")
#def topic_detail(request):
#    topics = Topics.objects.all()
#    return render(request, "blog/topic.html", {"topics": topics})

###################################################################
# Comment Views

def detail_comment(request, pk, topic_id):
    comment = Comments.objects.get(pk=pk)
    topic = Topics.objects.get(id=topic_id)
    return render(request, "blog/detail_comment.html", {"comment": comment, "topic":topic})
