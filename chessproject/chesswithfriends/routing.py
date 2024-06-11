from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
	# path('ws/socket-server/', consumers.chesswithfriendsConsumer.as_asgi()),
	re_path('withfriend/(?P<teamname>[a-zA-Z0-9]{8})/', consumers.OnlineWithFriendConsumer.as_asgi()),
	re_path('computer/(?P<token_id>[a-zA-Z0-9]{10})/', consumers.WithComputerConsumer.as_asgi()),
]