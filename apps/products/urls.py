from django.urls import path

from .views import ProductDetailView, ProductListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]
