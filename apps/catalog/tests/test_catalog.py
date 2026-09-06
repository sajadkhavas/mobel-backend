import pytest
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse

from apps.catalog.models import (
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


@pytest.mark.django_db
def test_catalog_taxonomy_contract_is_stable_when_empty(client):
    body = client.get(reverse("catalog-taxonomy")).json()

    assert set(body) == {
        "categories",
        "collections",
        "brands",
        "styles",
        "materials",
        "colors",
        "fabrics",
        "tags",
        "attributes",
    }
    assert all(value == [] for value in body.values())


@pytest.mark.django_db
def test_categories_expose_parent_slug_and_hide_inactive_rows(client):
    parent = Category.objects.create(name="Sofas", slug="sofas")
    Category.objects.create(name="Sectional", slug="sectional", parent=parent)
    Category.objects.create(name="Hidden", slug="hidden", is_active=False)

    body = client.get(reverse("catalog-categories")).json()
    by_slug = {item["slug"]: item for item in body}

    assert set(by_slug) == {"sofas", "sectional"}
    assert by_slug["sofas"]["parent_slug"] is None
    assert by_slug["sectional"]["parent_slug"] == "sofas"


@pytest.mark.django_db
def test_attributes_only_embed_active_values(client):
    attribute = Attribute.objects.create(
        name="Seat count",
        key="seat-count",
        is_filterable=True,
        is_variant_axis=True,
    )
    AttributeValue.objects.create(attribute=attribute, value="Three", slug="three")
    AttributeValue.objects.create(
        attribute=attribute,
        value="Hidden",
        slug="hidden",
        is_active=False,
    )

    body = client.get(reverse("catalog-taxonomy")).json()

    assert len(body["attributes"]) == 1
    assert body["attributes"][0]["key"] == "seat-count"
    assert [item["slug"] for item in body["attributes"][0]["values"]] == ["three"]


@pytest.mark.django_db
def test_category_hierarchy_rejects_cycles():
    root = Category.objects.create(name="Root", slug="root")
    child = Category.objects.create(name="Child", slug="child", parent=root)
    root.parent = child

    with pytest.raises(ValidationError):
        root.full_clean()


@pytest.mark.django_db
def test_color_validates_hex_code():
    color = Color(name="Cream", slug="cream", hex_code="cream")

    with pytest.raises(ValidationError):
        color.full_clean()


@pytest.mark.django_db
def test_attribute_value_slug_is_unique_per_attribute():
    attribute = Attribute.objects.create(name="Color", key="color")
    AttributeValue.objects.create(attribute=attribute, value="Blue", slug="blue")

    with pytest.raises(IntegrityError), transaction.atomic():
        AttributeValue.objects.create(attribute=attribute, value="Navy", slug="blue")


@pytest.mark.django_db
def test_catalog_models_are_registered_in_admin():
    for model in (
        Category,
        Collection,
        Brand,
        Style,
        Material,
        Color,
        Fabric,
        Tag,
        Attribute,
    ):
        assert admin.site.is_registered(model)
