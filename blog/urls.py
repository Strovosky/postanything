from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name='blog_home'),
    path("topic/<int:pk>/<int:user_id>", view=views.topic_detail_view, name="topic_detail"),
    path("comment/<int:pk>/<int:topic_id>", view=views.detail_comment, name="detail_comment")
    #path("topic/", view=views.topic_detail, name="topic")
]
