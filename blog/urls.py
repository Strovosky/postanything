from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name='blog_home'),
    #path("topic/<int:pk>/", view=views.TopicDetailView.as_view(), name="topic_detail")
    path("topic/", view=views.topic_detail, name="topic")
]