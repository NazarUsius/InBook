from django.urls import path
from . import views

urlpatterns = [
    path('', views.communities_list, name='communities_list'),
    path('create/', views.community_create, name='community_create'),
    path('edit/<int:pk>', views.community_edit, name='community_edit'),
    path('delete/<int:pk>', views.community_delete, name='community_delete'),
    path('detail/<int:pk>', views.community_detail, name='community_detail'),
    path('join/<int:pk>', views.community_join, name='community_join'),
    path('leave/<int:pk>', views.community_leave, name='community_leave'),
    path('like/<int:post_id>', views.post_like, name='post_like'),
    path('dislike/<int:post_id>', views.post_dislike, name='post_dislike'),
]
