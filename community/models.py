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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def user_liked(self, user):
        return user in self.likes.all()

    def user_disliked(self, user):
        return user in self.dislikes.all()

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"






