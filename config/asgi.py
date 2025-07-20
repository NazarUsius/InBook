import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

from chat import consumers


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"ws/chat/(?P<room_name>[\w_]+)/$", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})