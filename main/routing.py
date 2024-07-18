# main/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/valid/(?P<param1>[\w\s\d-]*)/$', consumers.ValidateConsumer.as_asgi()),
]