from django.db import models
from django.conf import settings

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members', blank=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='admins', blank=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    media = models.FileField(upload_to='media')
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

