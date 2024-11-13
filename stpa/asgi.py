# sales_tracker/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import sales_tracker.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stpa.settings')  # Update with your project settings path

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            sales_tracker.routing.websocket_urlpatterns
        )
    ),
})
