from django.core.exceptions import ValidationError
from django.db import models

from apps.catalog.models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Collection,
    Material,
    Style,
    Tag,
)
from apps.core.models import BaseModel


class Product(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    class FulfillmentMode(models.TextChoices):
        READY_TO_SHIP = "ready_to_ship", "Ready to ship"
        MADE_TO_ORDER = "made_to_order", "Made to order"
        MIXED = "mixed", "Ready stock + made to order"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    base_sku = models.CharField(max_length=64, unique=True)
    short_description = models.CharField(max_length=320, blank=True)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    fulfillment_mode = models.CharField(
        max_length=20,
        choices=FulfillmentMode.choices,
        default=FulfillmentMode.MADE_TO_ORDER,
    )
    production_lead_time_min_days = models.PositiveSmallIntegerField(default=0)
    production_lead_time_max_days = models.PositiveSmallIntegerField(default=0)
    availability_note = models.CharField(max_length=240, blank=True)
    customization_available = models.BooleanField(default=False)

    brand = models.ForeignKey(
        Brand,
        related_name="products",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    collections = models.ManyToManyField(Collection, related_name="products", blank=True)
    styles = models.ManyToManyField(Style, related_name="products", blank=True)
    materials = models.ManyToManyField(Material, related_name="products", blank=True)
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)

    class Meta:
        ordering = ("sort_order", "-published_at", "name")
        indexes = [
            models.Index(
                fields=("status", "is_active", "sort_order"),
                name="product_public_idx",
            )
        ]
        constraints = [
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
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        errors = {}
        if self.production_lead_time_max_days < self.production_lead_time_min_days:
            errors["production_lead_time_max_days"] = (
                "Maximum production lead time cannot be lower than minimum lead time."
            )
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            errors["published_at"] = "Published products require a publication date."
        if errors:
            raise ValidationError(errors)


class FurnitureSpecification(BaseModel):
    product = models.OneToOneField(
        Product,
        related_name="specification",
        on_delete=models.CASCADE,
    )
    seating_capacity = models.PositiveSmallIntegerField(null=True, blank=True)
    width_cm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    depth_cm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    seat_width_cm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    seat_depth_cm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    seat_height_cm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    arm_height_cm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    frame_material = models.CharField(max_length=160, blank=True)
    wood_type = models.CharField(max_length=160, blank=True)
    foam_type = models.CharField(max_length=160, blank=True)
    leg_material = models.CharField(max_length=160, blank=True)
    upholstery_notes = models.TextField(blank=True)
    care_instructions = models.TextField(blank=True)
    assembly_required = models.BooleanField(default=False)
    warranty_months = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Specifications: {self.product}"

    def clean(self):
        super().clean()
        errors = {}
        if self.seating_capacity is not None and self.seating_capacity < 1:
            errors["seating_capacity"] = "Seating capacity must be at least one."
        for field_name in (
            "width_cm",
            "depth_cm",
            "height_cm",
            "seat_width_cm",
            "seat_depth_cm",
            "seat_height_cm",
            "arm_height_cm",
            "weight_kg",
        ):
            value = getattr(self, field_name)
            if value is not None and value <= 0:
                errors[field_name] = "Measurement must be greater than zero."
        if errors:
            raise ValidationError(errors)


class ProductAttributeAssignment(BaseModel):
    product = models.ForeignKey(
        Product,
        related_name="attribute_assignments",
        on_delete=models.CASCADE,
    )
    attribute = models.ForeignKey(
        Attribute,
        related_name="product_assignments",
        on_delete=models.PROTECT,
    )
    selected_value = models.ForeignKey(
        AttributeValue,
        related_name="product_assignments",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    text_value = models.CharField(max_length=500, blank=True)
    number_value = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    boolean_value = models.BooleanField(null=True, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "created_at")
        constraints = [
            models.UniqueConstraint(
                fields=("product", "attribute"),
                name="unique_product_attribute",
            )
        ]

    def __str__(self):
        return f"{self.product} — {self.attribute}"

    def clean(self):
        super().clean()
        if not self.attribute_id:
            return

        errors = {}
        attribute = self.attribute
        if attribute.is_variant_axis:
            errors["attribute"] = "Variant-axis attributes are assigned in P04 variants."

        if self.selected_value_id and self.selected_value.attribute_id != self.attribute_id:
            errors["selected_value"] = "Selected value must belong to the assigned attribute."

        other_values_present = bool(self.text_value) or self.number_value is not None or (
            self.boolean_value is not None
        )

        if attribute.input_type in (Attribute.InputType.SELECT, Attribute.InputType.COLOR):
            if not self.selected_value_id:
                errors["selected_value"] = "This attribute requires a selected value."
            if other_values_present:
                errors["__all__"] = "Select/color attributes cannot store scalar values."
        elif attribute.input_type == Attribute.InputType.TEXT:
            if not self.text_value.strip():
                errors["text_value"] = "This attribute requires a text value."
            if (
                self.selected_value_id
                or self.number_value is not None
                or self.boolean_value is not None
            ):
                errors["__all__"] = "Text attributes can only store text_value."
        elif attribute.input_type == Attribute.InputType.NUMBER:
            if self.number_value is None:
                errors["number_value"] = "This attribute requires a number value."
            if self.selected_value_id or self.text_value or self.boolean_value is not None:
                errors["__all__"] = "Number attributes can only store number_value."
        elif attribute.input_type == Attribute.InputType.BOOLEAN:
            if self.boolean_value is None:
                errors["boolean_value"] = "This attribute requires a boolean value."
            if self.selected_value_id or self.text_value or self.number_value is not None:
                errors["__all__"] = "Boolean attributes can only store boolean_value."

        if errors:
            raise ValidationError(errors)
