from .consumers import DetectionConsumer
from django.urls import re_path


detection_urlpatterns = [
    re_path(r"ws/hid_detection/(?P<client>\w+)/$", DetectionConsumer.as_asgi()),
]