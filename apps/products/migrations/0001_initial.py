import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("catalog", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=220, unique=True)),
                ("base_sku", models.CharField(max_length=64, unique=True)),
                ("short_description", models.CharField(blank=True, max_length=320)),
                ("description", models.TextField(blank=True)),
                ("thumbnail_url", models.URLField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("published", "Published"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=16,
                    ),
                ),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                (
                    "fulfillment_mode",
                    models.CharField(
                        choices=[
                            ("ready_to_ship", "Ready to ship"),
                            ("made_to_order", "Made to order"),
                            ("mixed", "Ready stock + made to order"),
                        ],
                        default="made_to_order",
                        max_length=20,
                    ),
                ),
                ("production_lead_time_min_days", models.PositiveSmallIntegerField(default=0)),
                ("production_lead_time_max_days", models.PositiveSmallIntegerField(default=0)),
                ("availability_note", models.CharField(blank=True, max_length=240)),
                ("customization_available", models.BooleanField(default=False)),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="products",
                        to="catalog.brand",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="products",
                        to="catalog.category",
                    ),
                ),
                (
                    "collections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="products",
                        to="catalog.collection",
                    ),
                ),
                (
                    "materials",
                    models.ManyToManyField(
                        blank=True,
                        related_name="products",
                        to="catalog.material",
                    ),
                ),
                (
                    "styles",
                    models.ManyToManyField(blank=True, related_name="products", to="catalog.style"),
                ),
                (
                    "tags",
                    models.ManyToManyField(blank=True, related_name="products", to="catalog.tag"),
                ),
            ],
            options={
                "ordering": ("sort_order", "-published_at", "name"),
                "indexes": [
                    models.Index(
                        fields=["status", "is_active", "sort_order"],
                        name="product_public_idx",
                    )
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(
                            production_lead_time_max_days__gte=models.F(
                                "production_lead_time_min_days"
                            )
                        ),
                        name="product_lead_time_order",
                    ),
                    models.CheckConstraint(
                        condition=~models.Q(status="published")
                        | models.Q(published_at__isnull=False),
                        name="published_product_has_date",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="FurnitureSpecification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("seating_capacity", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "width_cm",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                (
                    "depth_cm",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                (
                    "height_cm",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                (
                    "seat_width_cm",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                (
                    "seat_depth_cm",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                (
                    "seat_height_cm",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                (
                    "arm_height_cm",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                (
                    "weight_kg",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                ("frame_material", models.CharField(blank=True, max_length=160)),
                ("wood_type", models.CharField(blank=True, max_length=160)),
                ("foam_type", models.CharField(blank=True, max_length=160)),
                ("leg_material", models.CharField(blank=True, max_length=160)),
                ("upholstery_notes", models.TextField(blank=True)),
                ("care_instructions", models.TextField(blank=True)),
                ("assembly_required", models.BooleanField(default=False)),
                ("warranty_months", models.PositiveSmallIntegerField(default=0)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specification",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductAttributeAssignment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("text_value", models.CharField(blank=True, max_length=500)),
                (
                    "number_value",
                    models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True),
                ),
                ("boolean_value", models.BooleanField(blank=True, null=True)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_assignments",
                        to="catalog.attribute",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attribute_assignments",
                        to="products.product",
                    ),
                ),
                (
                    "selected_value",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_assignments",
                        to="catalog.attributevalue",
                    ),
                ),
            ],
            options={
                "ordering": ("sort_order", "created_at"),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("product", "attribute"),
                        name="unique_product_attribute",
                    )
                ],
            },
        ),
    ]
