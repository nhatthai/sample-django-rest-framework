from django.urls import path
from accounts import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile-viewset', views.ProfileViewset, base_name='profiles')


urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns += router.urls
