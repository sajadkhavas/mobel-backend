from django.urls import path

from .views import categories, taxonomy

urlpatterns = [
    path("catalog/categories/", categories, name="catalog-categories"),
    path("catalog/taxonomy/", taxonomy, name="catalog-taxonomy"),
]
