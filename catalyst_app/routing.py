# yourapp/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/progress/', consumers.ProgressConsumer.as_asgi()),  # Define the WebSocket endpoint
]
