from django.urls import path
from . import views

urlpatterns = [
    path('', views.communities_list, name='community_list'),
    path('create/', views.community_create, name='community_create'),
    path('edit/<int:pk>', views.community_edit, name='community_edit'),
]
