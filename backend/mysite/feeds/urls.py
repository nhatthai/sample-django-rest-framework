from django.urls import path
from feeds import apis

urlpatterns = [
    path('feeds/', apis.FeedList.as_view()),
    path('feeds/<int:pk>/', apis.FeedDetail.as_view()),

    path('comments/', apis.CommentList.as_view()),
]
