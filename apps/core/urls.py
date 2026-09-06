from django.urls import path

from .views import readiness

urlpatterns = [
    path("system/ready/", readiness, name="system-ready"),
]
