from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/websocket_connect$', consumers.ListDataConsumer),
    re_path(r'ws/remote_control$', consumers.RemoteControl),
    # re_path(r'ws/statusWarningMonitor$', consumers.statusWarningMonitor)
]