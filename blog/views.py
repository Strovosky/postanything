from django.shortcuts import render

# Models
from .models import Subcomments, Topics, Comments
from django.contrib.auth.models import User

# Alerts
from django.contrib import messages

# Security
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'blog/index.html')


###################################################################
# Topic Views

# We will use a function view instead of a class view cuz we neeed the view to handle GET and POST 
# requests since we'll be creating comments.
@login_required(login_url="/login/")
def topic_detail_view(request, pk, user_id):
    if request.method == "POST":
        topic = Topics.objects.get(pk=pk)
        user = User.objects.get(id=user_id)
        topic_comments = Comments.objects.filter(topic=topic)
        subcomments = Subcomments.objects.all()

        for comment in Comments.objects.all():
            if request.POST.get("likes") == "like" + str(comment.id):
                comment.num_likes += 1
                comment.save()

        # If a subcomment was created
        for comment in topic.comments_set.all():
            if request.POST.get("btn_subcomment") == str(comment.id):
                content = request.POST.get("txt_subcomment")
                subcomment = Subcomments.objects.create(content=content, author=user, parent_comment=comment)
                subcomment.save()

        # If a comment was created
        if request.POST.get("btn_comment") == "comment_pressed":
            Comments.objects.create(content=request.POST.get("new_comment"), author=user, topic=topic)
            messages.success(request, "Comment created")
        return render(request, "blog/topic.html", {"topic_comments":topic_comments, "topic":topic, "subcomments":subcomments})
    else:
        topic = Topics.objects.get(pk=pk)
        topic_comments = Comments.objects.filter(topic=topic)
        return render(request, "blog/topic.html", {"topic":topic, "topic_comments":topic_comments})


@login_required(login_url="/login/")
def my_read_topics(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "blog/my_topics.html", {"topics":user.profile.topics_read.all()})


###################################################################
# Comment Views

def detail_comment(request, pk, topic_id):
    comment = Comments.objects.get(pk=pk)
    topic = Topics.objects.get(id=topic_id)
    return render(request, "blog/detail_comment.html", {"comment": comment, "topic":topic})
