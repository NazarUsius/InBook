from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('list', views.FriendsList, name='friends_list'),
    path('request/<str:second>', views.FriendsRequest, name='friends_request'),
]
