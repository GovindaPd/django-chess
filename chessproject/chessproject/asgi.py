import os
from django.core.asgi import get_asgi_application
# from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chesswithfriends.routing
# import routerhandling.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chessproject.settings')

application = ProtocolTypeRouter({
	'http':get_asgi_application(),
	'websocket': AuthMiddlewareStack(
		URLRouter(
			chesswithfriends.routing.websocket_urlpatterns
			# routerhandling.routing.websocket_urlpatterns
		)
	),
})
