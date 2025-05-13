from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
