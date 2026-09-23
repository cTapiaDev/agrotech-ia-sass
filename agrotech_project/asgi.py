import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import agronomy.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrotech_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            agronomy.routing.websocket_urlpatterns
        )
    ),
})
