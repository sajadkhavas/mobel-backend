from rest_framework import serializers

from .models import SocialLink, StoreLocation, StoreSettings


class StoreSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSettings
        fields = (
            "name",
            "legal_name",
            "tagline",
            "logo_url",
            "favicon_url",
            "primary_color",
            "secondary_color",
            "accent_color",
            "phone",
            "support_phone",
            "whatsapp",
            "email",
            "currency_code",
            "price_display_unit",
            "locale",
            "timezone",
        )


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ("key", "platform", "label", "url", "username")


class StoreLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreLocation
        fields = (
            "name",
            "slug",
            "location_type",
            "province",
            "city",
            "address",
            "postal_code",
            "phone",
            "whatsapp",
            "latitude",
            "longitude",
            "map_url",
            "working_hours",
            "is_primary",
        )
