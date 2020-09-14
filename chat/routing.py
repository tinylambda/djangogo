from django.urls import re_path

from . import consumers


websocket_patterns = [
    re_path(r'ws/chat/(?<room_name>\w+)/$', consumers.ChatConsumer),
]
