from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/consumer/<str:username>/',consumers.SocketConsumer.as_asgi()),
    path('ws/privateRoomConsumer/<str:username>/<str:roomname>/<str:is_host>/',consumers.privateSocketConsumer.as_asgi()),
]