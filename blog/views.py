from django.shortcuts import render

# For Class-based Views
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from .models import Topics, Comments
from django.contrib.auth.models import User

# Forms
from .forms import NewComment

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
        if form.is_valid():
            topic = Topics.objects.get(pk=pk)
            user = User.objects.get(id=user_id)
            Comments.objects.create(content=form.cleaned_data["comment"], author=user, topic=topic)
            topic_comments = Comments.objects.filter(topic=topic)
            messages.success(request, "Comment created")
            return render(request, "blog/topic.html", {"form":form, "topic_comments":topic_comments, "topic":topic})
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
