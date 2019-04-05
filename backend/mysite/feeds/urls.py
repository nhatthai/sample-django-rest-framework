from django.urls import path
from feeds import apis

urlpatterns = [
    path('feeds/', apis.FeedList.as_view()),
    path('feeds/<int:pk>/', apis.FeedDetail.as_view()),
    path('feeds/<int:pk>/emotions/', apis.EmotionList.as_view()),
    path('feeds/<int:pk>/comments/', apis.CommentList.as_view()),
    path('comments/<int:pk>/', apis.CommentDetail.as_view()),

    # delete emotion or update emotion
    path(
        'feeds/<int:pk>/emotions/<int:id>/',
        apis.EmotionDetail.as_view()),
]
