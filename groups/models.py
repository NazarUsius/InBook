from django.conf import settings
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')

    def __str__(self):
        return self.name
