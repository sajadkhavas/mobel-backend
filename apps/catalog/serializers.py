from rest_framework import serializers

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


class CategorySerializer(serializers.ModelSerializer):
    parent_slug = serializers.SlugRelatedField(
        source="parent",
        slug_field="slug",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "description",
            "parent_slug",
            "image_url",
            "is_featured",
            "sort_order",
        )


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            "name",
            "slug",
            "description",
            "image_url",
            "banner_url",
            "is_featured",
            "sort_order",
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("name", "slug", "description", "logo_url", "website_url", "sort_order")


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ("name", "slug", "description", "image_url", "sort_order")


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ("name", "slug", "description", "sort_order")


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("name", "slug", "description", "hex_code", "swatch_url", "sort_order")


class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = ("name", "slug", "description", "code", "swatch_url", "sort_order")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "slug", "description", "sort_order")


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ("value", "slug", "color_hex", "sort_order")


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, source="active_values", read_only=True)

    class Meta:
        model = Attribute
        fields = (
            "name",
            "key",
            "input_type",
            "is_filterable",
            "is_variant_axis",
            "sort_order",
            "values",
        )
