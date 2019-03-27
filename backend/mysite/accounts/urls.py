from django.urls import path
from django.conf.urls import url

from accounts import views

from rest_framework import routers


df_router = routers.DefaultRouter()
# df_router.register(
#     prefix='profiles', viewset=views.ProfileViewset, basename='profiles')

urlpatterns = [
    path('profiles/', views.profile_list),
    path('profiles/<int:pk>/', views.profile_detail),
]

urlpatterns += df_router.urls
