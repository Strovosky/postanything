from django.shortcuts import render
from django.views.generic import DetailView
from .models import Topics, Comments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'blog/index.html')

class TopicDetailView(DetailView):
    model = Topics
    template_name: str = "blog/topic.html"

@login_required(login_url="login/")
def topic_detail(request):
    topics = Topics.objects.all()
    return render(request, "blog/topic.html", {"topics": topics})
