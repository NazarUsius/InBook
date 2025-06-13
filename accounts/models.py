from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'Чоловік'),
        ('female', 'Жінка'),
        ('other', 'Інше'),
    ]

    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",  # Changed related_name
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Changed related_name
        related_query_name="user",
    )

    def __str__(self):
        return self.username
