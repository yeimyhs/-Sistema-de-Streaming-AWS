import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import streaming.routing  # Importa las rutas de WebSockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streamingproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Para peticiones HTTP normales
    "websocket": AuthMiddlewareStack(  # Para WebSockets
        URLRouter(streaming.routing.websocket_urlpatterns)
    ),
})
