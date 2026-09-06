import re

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel


class StoreSettings(BaseModel):
    class PriceDisplayUnit(models.TextChoices):
        RIAL = "rial", "ریال"
        TOMAN = "toman", "تومان"

    singleton_key = models.CharField(max_length=32, default="default", unique=True, editable=False)
    name = models.CharField(max_length=160, default="Mobel")
    legal_name = models.CharField(max_length=200, blank=True)
    tagline = models.CharField(max_length=240, blank=True)
    logo_url = models.URLField(blank=True)
    favicon_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=7, default="#111111")
    secondary_color = models.CharField(max_length=7, default="#F5F5F5")
    accent_color = models.CharField(max_length=7, default="#A67C52")
    phone = models.CharField(max_length=32, blank=True)
    support_phone = models.CharField(max_length=32, blank=True)
    whatsapp = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    currency_code = models.CharField(max_length=3, default="IRR")
    price_display_unit = models.CharField(
        max_length=8,
        choices=PriceDisplayUnit.choices,
        default=PriceDisplayUnit.TOMAN,
    )
    locale = models.CharField(max_length=16, default="fa-IR")
    timezone = models.CharField(max_length=64, default="Asia/Tehran")

    class Meta:
        verbose_name = "Store settings"
        verbose_name_plural = "Store settings"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        errors = {}
        for field_name in ("primary_color", "secondary_color", "accent_color"):
            value = getattr(self, field_name)
            if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
                errors[field_name] = "Use a six-digit hexadecimal color such as #A67C52."
        if errors:
            raise ValidationError(errors)


class SocialLink(BaseModel):
    class Platform(models.TextChoices):
        INSTAGRAM = "instagram", "Instagram"
        TELEGRAM = "telegram", "Telegram"
        WHATSAPP = "whatsapp", "WhatsApp"
        LINKEDIN = "linkedin", "LinkedIn"
        X = "x", "X"
        YOUTUBE = "youtube", "YouTube"
        APARAT = "aparat", "Aparat"
        PINTEREST = "pinterest", "Pinterest"
        OTHER = "other", "Other"

    key = models.SlugField(max_length=64, unique=True)
    platform = models.CharField(max_length=32, choices=Platform.choices)
    label = models.CharField(max_length=80, blank=True)
    url = models.URLField()
    username = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "key")

    def __str__(self):
        return self.label or self.key


class StoreLocation(BaseModel):
    class LocationType(models.TextChoices):
        SHOWROOM = "showroom", "Showroom"
        STORE = "store", "Store"
        WAREHOUSE = "warehouse", "Warehouse"
        OFFICE = "office", "Office"

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    location_type = models.CharField(
        max_length=16,
        choices=LocationType.choices,
        default=LocationType.SHOWROOM,
    )
    province = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    whatsapp = models.CharField(max_length=32, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_url = models.URLField(blank=True)
    working_hours = models.JSONField(default=dict, blank=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("is_primary",),
                condition=models.Q(is_primary=True),
                name="one_primary_store_location",
            )
        ]

    def __str__(self):
        return self.name


class FeatureFlag(BaseModel):
    class FeatureKey(models.TextChoices):
        ONLINE_PAYMENT = "online_payment", "Online payment"
        SHOW_PRICES = "show_prices", "Show prices"
        REVIEWS = "reviews", "Reviews"
        WISHLIST = "wishlist", "Wishlist"
        COMPARISON = "comparison", "Comparison"
        CUSTOM_ORDERS = "custom_orders", "Custom orders"
        REQUEST_QUOTE = "request_quote", "Request quote"
        CONSULTATION = "consultation", "Consultation"
        BLOG = "blog", "Blog"
        DISCOUNTS = "discounts", "Discounts"
        INVENTORY = "inventory", "Inventory"

    DEFAULTS = {
        FeatureKey.ONLINE_PAYMENT: False,
        FeatureKey.SHOW_PRICES: True,
        FeatureKey.REVIEWS: True,
        FeatureKey.WISHLIST: True,
        FeatureKey.COMPARISON: True,
        FeatureKey.CUSTOM_ORDERS: True,
        FeatureKey.REQUEST_QUOTE: True,
        FeatureKey.CONSULTATION: True,
        FeatureKey.BLOG: True,
        FeatureKey.DISCOUNTS: True,
        FeatureKey.INVENTORY: True,
    }

    key = models.CharField(max_length=64, choices=FeatureKey.choices, unique=True)
    enabled = models.BooleanField(default=True)
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("key",)

    def __str__(self):
        return self.key

    @classmethod
    def resolved(cls):
        flags = {
            str(key): {"enabled": enabled, "config": {}}
            for key, enabled in cls.DEFAULTS.items()
        }
        for flag in cls.objects.all().only("key", "enabled", "config"):
            flags[flag.key] = {"enabled": flag.enabled, "config": flag.config}
        return flags
