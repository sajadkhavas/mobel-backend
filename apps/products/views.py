from django.db.models import Prefetch, Q
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.catalog.models import Category, Collection, Material, Style, Tag

from .models import Product, ProductAttributeAssignment
from .serializers import ProductDetailSerializer, ProductListSerializer


def public_product_queryset(*, include_detail=False):
    queryset = (
        Product.objects.filter(
            status=Product.Status.PUBLISHED,
            is_active=True,
            published_at__lte=timezone.now(),
        )
        .select_related("brand", "specification")
        .prefetch_related(
            Prefetch(
                "categories",
                queryset=Category.objects.filter(is_active=True),
                to_attr="active_categories",
            ),
            Prefetch(
                "styles",
                queryset=Style.objects.filter(is_active=True),
                to_attr="active_styles",
            ),
        )
    )

    if not include_detail:
        return queryset

    active_assignments = (
        ProductAttributeAssignment.objects.filter(attribute__is_active=True)
        .filter(Q(selected_value__isnull=True) | Q(selected_value__is_active=True))
        .select_related("attribute", "selected_value")
        .order_by("sort_order", "attribute__sort_order", "attribute__name")
    )
    return queryset.prefetch_related(
        Prefetch(
            "collections",
            queryset=Collection.objects.filter(is_active=True),
            to_attr="active_collections",
        ),
        Prefetch(
            "materials",
            queryset=Material.objects.filter(is_active=True),
            to_attr="active_materials",
        ),
        Prefetch(
            "tags",
            queryset=Tag.objects.filter(is_active=True),
            to_attr="active_tags",
        ),
        Prefetch(
            "attribute_assignments",
            queryset=active_assignments,
            to_attr="active_attribute_assignments",
        ),
    )


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return public_product_queryset()


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return public_product_queryset(include_detail=True)
