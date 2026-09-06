import pytest
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse

from apps.store.models import FeatureFlag, SocialLink, StoreLocation, StoreSettings


@pytest.mark.django_db
def test_seeded_storefront_config_contract(client):
    response = client.get(reverse("storefront-config"))

    assert response.status_code == 200
    body = response.json()
    assert body["store"]["name"] == "Mobel"
    assert body["store"]["currency_code"] == "IRR"
    assert body["store"]["price_display_unit"] == "toman"
    assert body["features"]["online_payment"]["enabled"] is False
    assert body["features"]["show_prices"]["enabled"] is True
    assert set(body) == {"store", "social_links", "locations", "features"}


@pytest.mark.django_db
def test_storefront_config_only_exposes_active_socials_and_locations(client):
    SocialLink.objects.create(
        key="instagram-main",
        platform=SocialLink.Platform.INSTAGRAM,
        url="https://example.com/instagram",
        is_active=True,
    )
    SocialLink.objects.create(
        key="hidden-social",
        platform=SocialLink.Platform.OTHER,
        url="https://example.com/hidden",
        is_active=False,
    )
    StoreLocation.objects.create(name="Main showroom", slug="main-showroom", is_primary=True)
    StoreLocation.objects.create(
        name="Hidden warehouse",
        slug="hidden-warehouse",
        location_type=StoreLocation.LocationType.WAREHOUSE,
        is_active=False,
    )

    body = client.get(reverse("storefront-config")).json()

    assert [item["key"] for item in body["social_links"]] == ["instagram-main"]
    assert [item["slug"] for item in body["locations"]] == ["main-showroom"]


@pytest.mark.django_db
def test_only_one_primary_location_is_allowed():
    StoreLocation.objects.create(name="First", slug="first", is_primary=True)

    with pytest.raises(IntegrityError), transaction.atomic():
        StoreLocation.objects.create(name="Second", slug="second", is_primary=True)


@pytest.mark.django_db
def test_feature_defaults_are_stable_when_a_row_is_missing():
    FeatureFlag.objects.filter(key=FeatureFlag.FeatureKey.WISHLIST).delete()

    resolved = FeatureFlag.resolved()

    assert resolved["wishlist"] == {"enabled": True, "config": {}}


@pytest.mark.django_db
def test_store_settings_validates_brand_colors():
    store = StoreSettings.objects.get(singleton_key="default")
    store.primary_color = "red"

    with pytest.raises(ValidationError):
        store.full_clean()


@pytest.mark.django_db
def test_store_models_are_registered_in_admin():
    assert admin.site.is_registered(StoreSettings)
    assert admin.site.is_registered(SocialLink)
    assert admin.site.is_registered(StoreLocation)
    assert admin.site.is_registered(FeatureFlag)
