from django.urls import re_path, path
from .consumers import ChatConsumer,ComentarioConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),  # Ruta WebSocket
    re_path(r"ws/comentarios/(?P<idstreaming>\d+)/$", ComentarioConsumer.as_asgi()),
    #re_path(r"ws/comentarios/$", ComentarioConsumer.as_asgi()),
    #path("ws/chatgrupal/<str:sala>/", ChatgrupalConsumer.as_asgi()),
    
]
