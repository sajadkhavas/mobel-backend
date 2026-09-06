from django.contrib import admin

from .models import FurnitureSpecification, Product, ProductAttributeAssignment


class FurnitureSpecificationInline(admin.StackedInline):
    model = FurnitureSpecification
    extra = 0
    max_num = 1


class ProductAttributeAssignmentInline(admin.TabularInline):
    model = ProductAttributeAssignment
    extra = 0
    fields = (
        "attribute",
        "selected_value",
        "text_value",
        "number_value",
        "boolean_value",
        "sort_order",
    )
    ordering = ("sort_order", "created_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "base_sku",
        "status",
        "fulfillment_mode",
        "brand",
        "is_active",
        "is_featured",
        "updated_at",
    )
    list_filter = (
        "status",
        "fulfillment_mode",
        "is_active",
        "is_featured",
        "categories",
        "styles",
    )
    search_fields = ("name", "slug", "base_sku", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("brand", "categories", "collections", "styles", "materials", "tags")
    ordering = ("sort_order", "name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "name",
                    "slug",
                    "base_sku",
                    "short_description",
                    "description",
                    "thumbnail_url",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "status",
                    "published_at",
                    "is_active",
                    "is_featured",
                    "sort_order",
                )
            },
        ),
        (
            "Fulfillment",
            {
                "fields": (
                    "fulfillment_mode",
                    "production_lead_time_min_days",
                    "production_lead_time_max_days",
                    "availability_note",
                    "customization_available",
                )
            },
        ),
        (
            "Catalog",
            {"fields": ("brand", "categories", "collections", "styles", "materials", "tags")},
        ),
        ("System", {"fields": ("created_at", "updated_at")}),
    )
    inlines = (FurnitureSpecificationInline, ProductAttributeAssignmentInline)


@admin.register(FurnitureSpecification)
class FurnitureSpecificationAdmin(admin.ModelAdmin):
    list_display = ("product", "seating_capacity", "width_cm", "depth_cm", "height_cm")
    search_fields = ("product__name", "product__base_sku")
    autocomplete_fields = ("product",)


@admin.register(ProductAttributeAssignment)
class ProductAttributeAssignmentAdmin(admin.ModelAdmin):
    list_display = ("product", "attribute", "selected_value", "sort_order", "updated_at")
    list_filter = ("attribute",)
    search_fields = ("product__name", "product__base_sku", "attribute__name", "attribute__key")
    autocomplete_fields = ("product", "attribute")
    ordering = ("product", "sort_order")
