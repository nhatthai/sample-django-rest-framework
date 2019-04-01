from django.urls import path
from accounts import views, apis

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile-viewset', views.ProfileViewset, base_name='profiles')


urlpatterns = [
    path('profiles/', apis.ProfileList.as_view()),
    path('profiles/<int:pk>/', apis.ProfileDetail.as_view()),

    path('users/', apis.UserList.as_view()),
    path('users/<int:pk>/', apis.UserDetail.as_view()),
    path('users/create/', apis.UserCreate.as_view()),

    path('auths/sign_in/', views.sign_in),
    path('auths/sign_out/', views.Logout.as_view()),
]

urlpatterns += router.urls
