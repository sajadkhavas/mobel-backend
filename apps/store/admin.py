from django.contrib import admin

from .models import FeatureFlag, SocialLink, StoreLocation, StoreSettings


@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "price_display_unit", "updated_at")
    readonly_fields = ("singleton_key", "created_at", "updated_at")
    fieldsets = (
        ("Identity", {"fields": ("name", "legal_name", "tagline", "logo_url", "favicon_url")}),
        ("Brand", {"fields": ("primary_color", "secondary_color", "accent_color")}),
        ("Contact", {"fields": ("phone", "support_phone", "whatsapp", "email")}),
        ("Commerce", {"fields": ("currency_code", "price_display_unit")}),
        ("Localization", {"fields": ("locale", "timezone")}),
        ("System", {"fields": ("singleton_key", "created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("key", "platform", "username", "is_active", "sort_order")
    list_filter = ("platform", "is_active")
    search_fields = ("key", "label", "username", "url")
    ordering = ("sort_order", "key")


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "location_type", "city", "is_primary", "is_active", "sort_order")
    list_filter = ("location_type", "is_primary", "is_active", "province", "city")
    search_fields = ("name", "city", "address", "phone")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ("key", "enabled", "updated_at")
    list_filter = ("enabled",)
    search_fields = ("key",)
    ordering = ("key",)
