"""
ASGI config for hotel_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from detection.routing import detection_urlpatterns

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": URLRouter(detection_urlpatterns)
})