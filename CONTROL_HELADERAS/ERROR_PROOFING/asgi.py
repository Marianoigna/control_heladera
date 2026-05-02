"""
ASGI config for ERROR_PROOFING project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import DASHBOARD_TEMP_VOLT.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERROR_PROOFING.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            DASHBOARD_TEMP_VOLT.routing.websocket_urlpatterns
        )
    ),
})
