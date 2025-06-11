import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Room, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await self.get_messages_serialized()
        for message in messages:
            await self.send(text_data=json.dumps({
                'type': 'history',
                'message': message['content'],
                'user': message['username'],
                'timestamp': message['timestamp'],
            }))


    @database_sync_to_async
    def get_messages_serialized(self):
        room, _ = Room.objects.get_or_create(name=self.room_name)
        msgs = Message.objects.filter(room=room).order_by('timestamp')[:50]
        return [{
            'content': m.content,
            'username': m.user.username,
            'timestamp': m.timestamp.isoformat()
        } for m in msgs]

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    @database_sync_to_async
    def get_messages(self):
        room, _ = Room.objects.get_or_create(name=self.room_name)
        return list(Message.objects.filter(room=room).order_by('timestamp')[:50])

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        if not self.scope["user"].is_authenticated:
            return

        username = self.scope["user"].username
        await self.save_message(username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': username,
            }
        )

    @database_sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        room, _ = Room.objects.get_or_create(name=self.room_name)
        Message.objects.create(user=user, room=room, content=message)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'user': event['user'],
        }))