from decimal import Decimal

import pytest
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

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
from apps.products.models import FurnitureSpecification, Product, ProductAttributeAssignment


def create_published_product(**overrides):
    defaults = {
        "name": "Nava Sofa",
        "slug": "nava-sofa",
        "base_sku": "NAVA-BASE",
        "status": Product.Status.PUBLISHED,
        "published_at": timezone.now(),
        "fulfillment_mode": Product.FulfillmentMode.MADE_TO_ORDER,
        "production_lead_time_min_days": 7,
        "production_lead_time_max_days": 14,
    }
    defaults.update(overrides)
    return Product.objects.create(**defaults)


@pytest.mark.django_db
def test_published_product_requires_publication_date():
    product = Product(
        name="No date",
        slug="no-date",
        base_sku="NO-DATE",
        status=Product.Status.PUBLISHED,
    )

    with pytest.raises(ValidationError):
        product.full_clean()


@pytest.mark.django_db
def test_product_rejects_reversed_lead_time_range():
    product = Product(
        name="Bad lead time",
        slug="bad-lead",
        base_sku="BAD-LEAD",
        production_lead_time_min_days=20,
        production_lead_time_max_days=10,
    )

    with pytest.raises(ValidationError):
        product.full_clean()


@pytest.mark.django_db
def test_furniture_specification_rejects_non_positive_measurements():
    product = Product.objects.create(name="Chair", slug="chair", base_sku="CHAIR")
    specification = FurnitureSpecification(product=product, width_cm=Decimal("0"))

    with pytest.raises(ValidationError):
        specification.full_clean()


@pytest.mark.django_db
def test_product_attribute_assignment_enforces_non_variant_axis_and_value_ownership():
    product = Product.objects.create(name="Sofa", slug="sofa", base_sku="SOFA")
    variant_attribute = Attribute.objects.create(
        name="Fabric color",
        key="fabric-color",
        input_type=Attribute.InputType.COLOR,
        is_variant_axis=True,
    )
    variant_value = AttributeValue.objects.create(
        attribute=variant_attribute,
        value="Cream",
        slug="cream",
    )

    with pytest.raises(ValidationError):
        ProductAttributeAssignment(
            product=product,
            attribute=variant_attribute,
            selected_value=variant_value,
        ).full_clean()

    firmness = Attribute.objects.create(
        name="Firmness",
        key="firmness",
        input_type=Attribute.InputType.SELECT,
    )
    other = Attribute.objects.create(
        name="Room",
        key="room",
        input_type=Attribute.InputType.SELECT,
    )
    wrong_value = AttributeValue.objects.create(attribute=other, value="Living", slug="living")

    with pytest.raises(ValidationError):
        ProductAttributeAssignment(
            product=product,
            attribute=firmness,
            selected_value=wrong_value,
        ).full_clean()


@pytest.mark.django_db
def test_public_product_list_filters_visibility_and_has_bounded_query_count(client):
    category = Category.objects.create(name="Sofas", slug="sofas")
    style = Style.objects.create(name="Modern", slug="modern")
    for index in range(5):
        product = create_published_product(
            name=f"Sofa {index}",
            slug=f"sofa-{index}",
            base_sku=f"SOFA-{index}",
            sort_order=index,
        )
        product.categories.add(category)
        product.styles.add(style)

    Product.objects.create(name="Draft", slug="draft", base_sku="DRAFT")
    create_published_product(
        name="Inactive",
        slug="inactive",
        base_sku="INACTIVE",
        is_active=False,
    )
    create_published_product(
        name="Future",
        slug="future",
        base_sku="FUTURE",
        published_at=timezone.now() + timezone.timedelta(days=1),
    )

    with CaptureQueriesContext(connection) as queries:
        response = client.get(reverse("products-list"))

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 5
    assert [item["slug"] for item in body["results"]] == [f"sofa-{i}" for i in range(5)]
    assert len(queries) <= 8


@pytest.mark.django_db
def test_product_detail_exposes_active_catalog_specification_and_non_variant_attributes(client):
    brand = Brand.objects.create(name="Mobel", slug="mobel")
    active_category = Category.objects.create(name="Sofas", slug="sofas")
    hidden_category = Category.objects.create(name="Hidden", slug="hidden", is_active=False)
    collection = Collection.objects.create(name="Living", slug="living")
    style = Style.objects.create(name="Modern", slug="modern")
    material = Material.objects.create(name="Beech", slug="beech")
    tag = Tag.objects.create(name="Featured", slug="featured")
    product = create_published_product(brand=brand)
    product.categories.add(active_category, hidden_category)
    product.collections.add(collection)
    product.styles.add(style)
    product.materials.add(material)
    product.tags.add(tag)
    FurnitureSpecification.objects.create(
        product=product,
        seating_capacity=3,
        width_cm=Decimal("220"),
        frame_material="Beech frame",
        foam_type="HR foam",
        warranty_months=24,
    )
    firmness = Attribute.objects.create(
        name="Firmness",
        key="firmness",
        input_type=Attribute.InputType.SELECT,
        is_filterable=True,
    )
    medium = AttributeValue.objects.create(attribute=firmness, value="Medium", slug="medium")
    ProductAttributeAssignment.objects.create(
        product=product,
        attribute=firmness,
        selected_value=medium,
    )
    hidden_attribute = Attribute.objects.create(
        name="Hidden attribute",
        key="hidden-attribute",
        input_type=Attribute.InputType.TEXT,
        is_active=False,
    )
    ProductAttributeAssignment.objects.create(
        product=product,
        attribute=hidden_attribute,
        text_value="secret",
    )

    response = client.get(reverse("product-detail", kwargs={"slug": product.slug}))

    assert response.status_code == 200
    body = response.json()
    assert body["brand"] == {"name": "Mobel", "slug": "mobel"}
    assert [item["slug"] for item in body["categories"]] == ["sofas"]
    assert [item["slug"] for item in body["collections"]] == ["living"]
    assert [item["slug"] for item in body["styles"]] == ["modern"]
    assert [item["slug"] for item in body["materials"]] == ["beech"]
    assert [item["slug"] for item in body["tags"]] == ["featured"]
    assert body["specification"]["seating_capacity"] == 3
    assert body["specification"]["frame_material"] == "Beech frame"
    assert [item["key"] for item in body["attributes"]] == ["firmness"]
    assert body["attributes"][0]["value"]["slug"] == "medium"


@pytest.mark.django_db
def test_product_models_are_registered_in_admin():
    for model in (Product, FurnitureSpecification, ProductAttributeAssignment):
        assert admin.site.is_registered(model)
