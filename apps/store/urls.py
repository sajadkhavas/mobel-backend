from django.urls import path

from .views import storefront_config

urlpatterns = [
    path("storefront/config/", storefront_config, name="storefront-config"),
]
