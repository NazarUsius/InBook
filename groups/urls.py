from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('list', views.group_list, name='group_list'),
    path('detail/<int:group_id>', views.group_detail, name='group_detail'),
    path('add/', views.group_add, name='group_add'),
    path('join/<int:group_id>', views.group_join, name='group_join'),
    path('leave/<int:group_id>', views.group_leave, name='group_leave'),
    path('send_message/<int:group_id>', views.group_send_message, name='group_send_message'),
]
