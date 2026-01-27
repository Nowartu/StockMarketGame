from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/stock/$", consumers.AsyncStockConsumer.as_asgi()),
    re_path(r"ws/order/$", consumers.AsyncOrderConsumer.as_asgi()),
]