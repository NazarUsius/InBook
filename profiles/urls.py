from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.ProfileView, name='profile'),
    path('change/user/', views.ChangeProfileView, name='profile_change'),
]
