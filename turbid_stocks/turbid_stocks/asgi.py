"""
ASGI config for turbid_stocks project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import stocks.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turbid_stocks.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            stocks.routing.websocket_urlpatterns
        )
    ),
})
