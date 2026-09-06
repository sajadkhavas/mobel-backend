from django.contrib import admin
from django.urls import include, path

from apps.core.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/", include("apps.store.urls")),
    path("api/v1/", include("apps.catalog.urls")),
    path("api/v1/", include("apps.products.urls")),
]
