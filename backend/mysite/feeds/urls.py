from django.urls import path
from feeds import apis

urlpatterns = [
    path('feeds/', apis.FeedList.as_view()),
    path('feeds/<int:pk>/', apis.FeedDetail.as_view()),
    path('feeds/<int:pk>/emotions/', apis.EmotionDetail.as_view()),

    path('comments/', apis.CommentList.as_view()),
    path('comments/<int:pk>/', apis.CommentDetail.as_view()),

]
