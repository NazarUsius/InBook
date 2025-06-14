from django.db import models
from django.conf import settings

class WebPushSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    endpoint = models.TextField()
    auth = models.CharField(max_length=256)
    p256dh = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
