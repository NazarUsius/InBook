from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Message

User = get_user_model()

@login_required
def room_list(request):
    rooms = request.user.rooms.all()  # комнаты, где участвует пользователь
    return render(request, 'chat/room_list.html', {'rooms': rooms})

@login_required
def room_detail(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.user not in room.participants.all():
        return redirect('chat:room_list')  # запрет доступа если не участник

    messages = room.messages.order_by('timestamp')
    return render(request, 'chat/room.html', {'room_name': room.name, 'messages': messages})

@login_required
def start_chat(request, user_id):
    # Начинаем чат с другим пользователем
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return redirect('chat:room_list')  # нельзя начать чат с самим собой

    room = Room.get_or_create_room(request.user, other_user)
    return redirect('chat:room_detail', room_name=room.name)
