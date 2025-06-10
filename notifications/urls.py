from django.urls import path
from .views import save_subscription, notify_users

urlpatterns = [
    path("subscribe/", save_subscription, name="save_subscription"),
]
