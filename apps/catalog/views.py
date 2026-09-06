from django.db.models import Prefetch
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Collection,
    Color,
    Fabric,
    Material,
    Style,
    Tag,
)
from .serializers import (
    AttributeSerializer,
    BrandSerializer,
    CategorySerializer,
    CollectionSerializer,
    ColorSerializer,
    FabricSerializer,
    MaterialSerializer,
    StyleSerializer,
    TagSerializer,
)


def active(queryset):
    return queryset.filter(is_active=True).order_by("sort_order", "name")


def category_queryset():
    return active(Category.objects.select_related("parent"))


def attribute_queryset():
    active_values = AttributeValue.objects.filter(is_active=True).order_by("sort_order", "value")
    return active(Attribute.objects.all()).prefetch_related(
        Prefetch("values", queryset=active_values, to_attr="active_values")
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def categories(request):
    return Response(CategorySerializer(category_queryset(), many=True).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def taxonomy(request):
    return Response(
        {
            "categories": CategorySerializer(category_queryset(), many=True).data,
            "collections": CollectionSerializer(active(Collection.objects.all()), many=True).data,
            "brands": BrandSerializer(active(Brand.objects.all()), many=True).data,
            "styles": StyleSerializer(active(Style.objects.all()), many=True).data,
            "materials": MaterialSerializer(active(Material.objects.all()), many=True).data,
            "colors": ColorSerializer(active(Color.objects.all()), many=True).data,
            "fabrics": FabricSerializer(active(Fabric.objects.all()), many=True).data,
            "tags": TagSerializer(active(Tag.objects.all()), many=True).data,
            "attributes": AttributeSerializer(attribute_queryset(), many=True).data,
        }
    )
