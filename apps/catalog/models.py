import re

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel

HEX_COLOR_PATTERN = re.compile(r"#[0-9A-Fa-f]{6}")


def validate_hex_color(value):
    if value and not HEX_COLOR_PATTERN.fullmatch(value):
        raise ValidationError("Use a six-digit hexadecimal color such as #A67C52.")


class CatalogTaxonomyModel(BaseModel):
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name


class Category(CatalogTaxonomyModel):
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta(CatalogTaxonomyModel.Meta):
        verbose_name_plural = "Categories"

    def clean(self):
        super().clean()
        if not self.parent_id:
            return
        if self.pk and self.parent_id == self.pk:
            raise ValidationError({"parent": "A category cannot be its own parent."})

        visited = {self.pk} if self.pk else set()
        ancestor = self.parent
        while ancestor is not None:
            if ancestor.pk in visited:
                raise ValidationError({"parent": "Category hierarchy cannot contain a cycle."})
            visited.add(ancestor.pk)
            ancestor = ancestor.parent


class Collection(CatalogTaxonomyModel):
    image_url = models.URLField(blank=True)
    banner_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)


class Brand(CatalogTaxonomyModel):
    logo_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)


class Style(CatalogTaxonomyModel):
    image_url = models.URLField(blank=True)


class Material(CatalogTaxonomyModel):
    pass


class Color(CatalogTaxonomyModel):
    hex_code = models.CharField(max_length=7, blank=True, validators=[validate_hex_color])
    swatch_url = models.URLField(blank=True)


class Fabric(CatalogTaxonomyModel):
    code = models.CharField(max_length=64, blank=True)
    swatch_url = models.URLField(blank=True)


class Tag(CatalogTaxonomyModel):
    pass


class Attribute(BaseModel):
    class InputType(models.TextChoices):
        SELECT = "select", "Select"
        COLOR = "color", "Color"
        BOOLEAN = "boolean", "Boolean"
        TEXT = "text", "Text"
        NUMBER = "number", "Number"

    name = models.CharField(max_length=160)
    key = models.SlugField(max_length=100, unique=True)
    input_type = models.CharField(
        max_length=16,
        choices=InputType.choices,
        default=InputType.SELECT,
    )
    is_filterable = models.BooleanField(default=False)
    is_variant_axis = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name


class AttributeValue(BaseModel):
    attribute = models.ForeignKey(
        Attribute,
        related_name="values",
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=160)
    slug = models.SlugField(max_length=120)
    color_hex = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_hex_color],
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "value")
        constraints = [
            models.UniqueConstraint(
                fields=("attribute", "slug"),
                name="unique_attribute_value_slug",
            )
        ]

    def __str__(self):
        return f"{self.attribute}: {self.value}"
