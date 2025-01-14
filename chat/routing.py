from django.urls import path
from chat import consumers


# WebSocket URL configuration
websocket_urlpatterns = [
    path("ws/sc/", consumers.SynchronousConsumer.as_asgi()),
    path("ws/ac/<str:group_name>/", consumers.AsynchronousConsumer.as_asgi()),
]