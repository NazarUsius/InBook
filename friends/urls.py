from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('list', views.friends_list, name='friends_list'),
    path('request/<str:second>', views.friends_request, name='friends_request'),
    path('accept/<str:iniciator>', views.friends_request_accept, name='friends_request_accept'),
    path('decline/<str:iniciator>', views.friends_request_decline, name='friends_request_decline'),
    path('delete/<int:second>', views.friends_delete, name='friends_delete'),


]
