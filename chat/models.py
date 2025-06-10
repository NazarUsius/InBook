from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Room(models.Model):
    # Уникальное имя комнаты, например "chat_3_7"
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rooms')

    def __str__(self):
        return self.name

    @staticmethod
    def get_room_name(user1_id, user2_id):
        # Генерируем имя комнаты в формате chat_3_7 (сортируем id)
        ids = sorted([user1_id, user2_id])
        return f"chat_{ids[0]}_{ids[1]}"

    @classmethod
    def get_or_create_room(cls, user1, user2):
        name = cls.get_room_name(user1.id, user2.id)
        room, created = cls.objects.get_or_create(name=name)
        if created:
            room.participants.add(user1, user2)
        return room


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.user.username}: {self.content}"
