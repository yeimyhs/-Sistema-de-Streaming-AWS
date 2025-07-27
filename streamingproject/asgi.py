import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streamingproject.settings')
django.setup()


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import streaming.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Para peticiones HTTP normales
    "websocket": AuthMiddlewareStack(  # Para WebSockets
        URLRouter(streaming.routing.websocket_urlpatterns)
    ),
})
