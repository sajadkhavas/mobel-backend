from django.contrib import admin

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


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")


@admin.register(Category)
class CategoryAdmin(TaxonomyAdmin):
    list_display = (
        "name",
        "parent",
        "is_featured",
        "is_active",
        "sort_order",
        "updated_at",
    )
    list_filter = ("is_featured", "is_active")
    autocomplete_fields = ("parent",)


@admin.register(Collection)
class CollectionAdmin(TaxonomyAdmin):
    list_display = ("name", "is_featured", "is_active", "sort_order", "updated_at")
    list_filter = ("is_featured", "is_active")


@admin.register(Brand)
class BrandAdmin(TaxonomyAdmin):
    pass


@admin.register(Style)
class StyleAdmin(TaxonomyAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(TaxonomyAdmin):
    pass


@admin.register(Color)
class ColorAdmin(TaxonomyAdmin):
    list_display = ("name", "hex_code", "is_active", "sort_order", "updated_at")


@admin.register(Fabric)
class FabricAdmin(TaxonomyAdmin):
    list_display = ("name", "code", "is_active", "sort_order", "updated_at")


@admin.register(Tag)
class TagAdmin(TaxonomyAdmin):
    pass


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 0
    fields = ("value", "slug", "color_hex", "is_active", "sort_order")
    prepopulated_fields = {"slug": ("value",)}
    ordering = ("sort_order", "value")


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "key",
        "input_type",
        "is_filterable",
        "is_variant_axis",
        "is_active",
        "sort_order",
    )
    list_filter = ("input_type", "is_filterable", "is_variant_axis", "is_active")
    search_fields = ("name", "key")
    prepopulated_fields = {"key": ("name",)}
    ordering = ("sort_order", "name")
    inlines = (AttributeValueInline,)
