from django.conf import settings
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='user_joined_groups',
        blank=True
    )

    def __str__(self):
        return self.name

    def is_member(self, user):
        if not user.is_authenticated:
            return False
        return self.members.filter(id=user.id).exists()



class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content}"
