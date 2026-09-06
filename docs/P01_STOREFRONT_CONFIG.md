# P01 — Storefront configuration contract

## Rule

Merchant-manageable storefront identity and business configuration is backend-authoritative. Lovable/React must consume this contract instead of hardcoding store identity, contact details, locations, social links, feature availability, price display units, or merchant-controlled brand colors.

Pure presentation concerns such as spacing, responsive breakpoints, animation timing, component composition, and accessibility behavior remain frontend-owned.

## Public endpoint

`GET /api/v1/storefront/config/`

The endpoint is intentionally public and read-only. It returns four stable top-level keys:

- `store`: identity, contact, localization and limited brand/theme settings.
- `social_links`: active links ordered by merchant-controlled sort order.
- `locations`: active showrooms/stores/warehouses/offices ordered by merchant-controlled sort order.
- `features`: stable feature-key mapping with `enabled` and future-safe `config` objects.

## Stable feature defaults

The API resolves known defaults even if a FeatureFlag row is accidentally missing. This prevents the frontend contract from silently changing shape.

Default disabled:
- `online_payment`

Default enabled:
- `show_prices`
- `reviews`
- `wishlist`
- `comparison`
- `custom_orders`
- `request_quote`
- `consultation`
- `blog`
- `discounts`
- `inventory`

## Admin ownership

Django Admin manages StoreSettings, SocialLink, StoreLocation and FeatureFlag. StoreSettings is a logical singleton: after the default settings row exists, the Admin does not allow adding another settings object.

## Media boundary

P01 stores logo/favicon references as URLs. The dedicated media pipeline and uploads belong to P05; the public API shape does not need to change when those URLs later come from managed media storage.
