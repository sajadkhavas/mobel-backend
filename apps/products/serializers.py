from rest_framework import serializers

from apps.catalog.models import Attribute

from .models import FurnitureSpecification, Product, ProductAttributeAssignment


class TaxonomyReferenceSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    slug = serializers.SlugField(read_only=True)


class FurnitureSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnitureSpecification
        fields = (
            "seating_capacity",
            "width_cm",
            "depth_cm",
            "height_cm",
            "seat_width_cm",
            "seat_depth_cm",
            "seat_height_cm",
            "arm_height_cm",
            "weight_kg",
            "frame_material",
            "wood_type",
            "foam_type",
            "leg_material",
            "upholstery_notes",
            "care_instructions",
            "assembly_required",
            "warranty_months",
        )


class ProductAttributeAssignmentSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source="attribute.key", read_only=True)
    name = serializers.CharField(source="attribute.name", read_only=True)
    input_type = serializers.CharField(source="attribute.input_type", read_only=True)
    value = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttributeAssignment
        fields = ("key", "name", "input_type", "value", "sort_order")

    def get_value(self, obj):
        if obj.attribute.input_type in (Attribute.InputType.SELECT, Attribute.InputType.COLOR):
            if obj.selected_value is None:
                return None
            return {
                "value": obj.selected_value.value,
                "slug": obj.selected_value.slug,
                "color_hex": obj.selected_value.color_hex,
            }
        if obj.attribute.input_type == Attribute.InputType.TEXT:
            return obj.text_value
        if obj.attribute.input_type == Attribute.InputType.NUMBER:
            return str(obj.number_value) if obj.number_value is not None else None
        if obj.attribute.input_type == Attribute.InputType.BOOLEAN:
            return obj.boolean_value
        return None


class ProductBaseSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    categories = TaxonomyReferenceSerializer(many=True, source="active_categories", read_only=True)
    styles = TaxonomyReferenceSerializer(many=True, source="active_styles", read_only=True)
    specification = FurnitureSpecificationSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "base_sku",
            "short_description",
            "thumbnail_url",
            "is_featured",
            "fulfillment_mode",
            "production_lead_time_min_days",
            "production_lead_time_max_days",
            "availability_note",
            "customization_available",
            "brand",
            "categories",
            "styles",
            "specification",
        )

    def get_brand(self, obj):
        if obj.brand_id is None or not obj.brand.is_active:
            return None
        return {"name": obj.brand.name, "slug": obj.brand.slug}


class ProductListSerializer(ProductBaseSerializer):
    pass


class ProductDetailSerializer(ProductBaseSerializer):
    collections = TaxonomyReferenceSerializer(
        many=True,
        source="active_collections",
        read_only=True,
    )
    materials = TaxonomyReferenceSerializer(many=True, source="active_materials", read_only=True)
    tags = TaxonomyReferenceSerializer(many=True, source="active_tags", read_only=True)
    attributes = ProductAttributeAssignmentSerializer(
        many=True,
        source="active_attribute_assignments",
        read_only=True,
    )

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + (
            "description",
            "published_at",
            "collections",
            "materials",
            "tags",
            "attributes",
        )
