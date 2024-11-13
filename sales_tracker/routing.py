# sales_tracker/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/screen_share/(?P<employee_id>\w+)/$', consumers.ScreenShareConsumer.as_asgi()),
]
