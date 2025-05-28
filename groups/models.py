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
        """Check if a user is a member of this group"""
        if not user.is_authenticated:
            return False
        return self.members.filter(id=user.id).exists()
