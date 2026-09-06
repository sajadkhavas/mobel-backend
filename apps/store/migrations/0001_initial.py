import uuid

from django.db import migrations, models


def seed_store_configuration(apps, schema_editor):
    StoreSettings = apps.get_model("store", "StoreSettings")
    FeatureFlag = apps.get_model("store", "FeatureFlag")

    StoreSettings.objects.get_or_create(
        singleton_key="default",
        defaults={
            "name": "Mobel",
            "currency_code": "IRR",
            "price_display_unit": "toman",
            "locale": "fa-IR",
            "timezone": "Asia/Tehran",
        },
    )

    defaults = {
        "online_payment": False,
        "show_prices": True,
        "reviews": True,
        "wishlist": True,
        "comparison": True,
        "custom_orders": True,
        "request_quote": True,
        "consultation": True,
        "blog": True,
        "discounts": True,
        "inventory": True,
    }
    for key, enabled in defaults.items():
        FeatureFlag.objects.get_or_create(key=key, defaults={"enabled": enabled, "config": {}})


def keep_merchant_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FeatureFlag",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "key",
                    models.CharField(
                        choices=[
                            ("online_payment", "Online payment"),
                            ("show_prices", "Show prices"),
                            ("reviews", "Reviews"),
                            ("wishlist", "Wishlist"),
                            ("comparison", "Comparison"),
                            ("custom_orders", "Custom orders"),
                            ("request_quote", "Request quote"),
                            ("consultation", "Consultation"),
                            ("blog", "Blog"),
                            ("discounts", "Discounts"),
                            ("inventory", "Inventory"),
                        ],
                        max_length=64,
                        unique=True,
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("config", models.JSONField(blank=True, default=dict)),
            ],
            options={"ordering": ("key",)},
        ),
        migrations.CreateModel(
            name="SocialLink",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("key", models.SlugField(max_length=64, unique=True)),
                (
                    "platform",
                    models.CharField(
                        choices=[
                            ("instagram", "Instagram"),
                            ("telegram", "Telegram"),
                            ("whatsapp", "WhatsApp"),
                            ("linkedin", "LinkedIn"),
                            ("x", "X"),
                            ("youtube", "YouTube"),
                            ("aparat", "Aparat"),
                            ("pinterest", "Pinterest"),
                            ("other", "Other"),
                        ],
                        max_length=32,
                    ),
                ),
                ("label", models.CharField(blank=True, max_length=80)),
                ("url", models.URLField()),
                ("username", models.CharField(blank=True, max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={"ordering": ("sort_order", "key")},
        ),
        migrations.CreateModel(
            name="StoreLocation",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160)),
                ("slug", models.SlugField(max_length=180, unique=True)),
                (
                    "location_type",
                    models.CharField(
                        choices=[
                            ("showroom", "Showroom"),
                            ("store", "Store"),
                            ("warehouse", "Warehouse"),
                            ("office", "Office"),
                        ],
                        default="showroom",
                        max_length=16,
                    ),
                ),
                ("province", models.CharField(blank=True, max_length=100)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("address", models.TextField(blank=True)),
                ("postal_code", models.CharField(blank=True, max_length=20)),
                ("phone", models.CharField(blank=True, max_length=32)),
                ("whatsapp", models.CharField(blank=True, max_length=32)),
                ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("map_url", models.URLField(blank=True)),
                ("working_hours", models.JSONField(blank=True, default=dict)),
                ("is_primary", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                "ordering": ("sort_order", "name"),
                "constraints": [
                    models.UniqueConstraint(
                        condition=models.Q(is_primary=True),
                        fields=("is_primary",),
                        name="one_primary_store_location",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="StoreSettings",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("singleton_key", models.CharField(default="default", editable=False, max_length=32, unique=True)),
                ("name", models.CharField(default="Mobel", max_length=160)),
                ("legal_name", models.CharField(blank=True, max_length=200)),
                ("tagline", models.CharField(blank=True, max_length=240)),
                ("logo_url", models.URLField(blank=True)),
                ("favicon_url", models.URLField(blank=True)),
                ("primary_color", models.CharField(default="#111111", max_length=7)),
                ("secondary_color", models.CharField(default="#F5F5F5", max_length=7)),
                ("accent_color", models.CharField(default="#A67C52", max_length=7)),
                ("phone", models.CharField(blank=True, max_length=32)),
                ("support_phone", models.CharField(blank=True, max_length=32)),
                ("whatsapp", models.CharField(blank=True, max_length=32)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("currency_code", models.CharField(default="IRR", max_length=3)),
                (
                    "price_display_unit",
                    models.CharField(
                        choices=[("rial", "ریال"), ("toman", "تومان")],
                        default="toman",
                        max_length=8,
                    ),
                ),
                ("locale", models.CharField(default="fa-IR", max_length=16)),
                ("timezone", models.CharField(default="Asia/Tehran", max_length=64)),
            ],
            options={
                "verbose_name": "Store settings",
                "verbose_name_plural": "Store settings",
            },
        ),
        migrations.RunPython(seed_store_configuration, keep_merchant_data),
    ]
