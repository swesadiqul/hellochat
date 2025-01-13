from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path("ws/sc/", consumers.SynchronousConsumer.as_asgi()),
    path("ws/ac/", consumers.AsynchronousConsumer.as_asgi()),
]