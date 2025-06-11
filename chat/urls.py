from django.urls import path
from . import views

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('<str:room_name>/', views.room_detail, name='room_detail'),
]