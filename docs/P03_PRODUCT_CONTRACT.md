# P03 — Furniture Product Engine Contract

## Purpose

P03 introduces the backend-authoritative furniture product domain. Lovable/React consumes the public API and must not hardcode merchant-managed product facts.

## Ownership boundaries

P03 owns:

- product identity (`name`, `slug`, `base_sku`)
- draft/published/archived lifecycle and publication scheduling
- active/featured merchandising controls
- ready-to-ship / made-to-order / mixed fulfillment mode
- production lead-time range and availability note
- customization availability
- catalog relations (category, collection, brand, style, material, tag)
- furniture dimensions and construction specifications
- non-variant typed product attributes
- one temporary `thumbnail_url` fallback

Deferred deliberately:

- P04: variant combinations, variant SKU/options
- P05: durable media library, gallery and image ownership
- P09: final pricing/cart pricing rules
- P15: SEO metadata/content schema

## Public APIs

### `GET /api/v1/products/`

Paginated public product list. Only rows meeting all conditions are returned:

- `status=published`
- `is_active=true`
- `published_at <= now`

List items expose identity, fulfillment summary, active brand/category/style references and furniture specification data. Draft, archived, inactive and future-scheduled products do not leak.

### `GET /api/v1/products/{slug}/`

Public detail endpoint using the same visibility rules. It additionally exposes:

- full description
- active collections/materials/tags
- active non-variant attribute assignments
- publication timestamp

Inactive taxonomy rows and inactive attribute/value rows are omitted from the public representation.

## Product attributes

`ProductAttributeAssignment` stores exactly one product-level attribute value. Variant-axis attributes are rejected in P03 because P04 owns variant combinations.

Storage by attribute type:

- `select` / `color`: `selected_value`
- `text`: `text_value`
- `number`: `number_value`
- `boolean`: `boolean_value`

The selected `AttributeValue` must belong to the assigned `Attribute`.

## Furniture specification

One optional `FurnitureSpecification` row may exist per product. It stores seating capacity, dimensions, weight, frame/wood/foam/leg construction, upholstery/care notes, assembly requirement and warranty months. Non-empty measurements must be greater than zero.

## Database invariants

- product `slug` is unique
- product `base_sku` is unique
- max lead time cannot be lower than min lead time
- a published product must have `published_at`
- one furniture specification per product
- one assignment per `(product, attribute)`

Django model validation adds user-facing errors before database constraint failures where applicable.

## Query contract

Public querysets explicitly use `select_related` for brand/specification and `Prefetch` for many-to-many taxonomies and attribute assignments. This is intentional: Django REST Framework does not automatically optimize serializer relationship queries.

## Frontend integration rule

Lovable may choose layout and presentation, but product facts, availability, specifications and catalog membership come from these APIs. The frontend must tolerate an empty `thumbnail_url` until P05 supplies the durable media/gallery layer.
