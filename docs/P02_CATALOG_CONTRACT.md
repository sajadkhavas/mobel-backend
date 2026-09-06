# P02 — Catalog Foundation Contract

## Backend ownership

Catalog taxonomy is merchant-managed in Django Admin and backend-authoritative. Lovable/React must consume the public APIs instead of hardcoding category trees, collections, brands, furniture styles, materials, colors, fabrics, tags, or filter/variant attributes.

## Public APIs

### `GET /api/v1/catalog/categories/`

Returns active categories as a flat ordered list. Each category carries `parent_slug`; the frontend can build navigation trees without requiring recursive API calls.

### `GET /api/v1/catalog/taxonomy/`

Returns stable top-level keys:

- `categories`
- `collections`
- `brands`
- `styles`
- `materials`
- `colors`
- `fabrics`
- `tags`
- `attributes`

Only active entities are exposed. Attributes include only active attribute values.

## Query policy

Category queries use `select_related("parent")`. Attribute values are fetched with an explicit filtered `Prefetch` into `active_values`. This keeps relational serialization explicit and avoids relation-driven N+1 queries as catalog size grows.

## Attribute model

Attributes are typed as `select`, `color`, `boolean`, `text`, or `number`. `is_filterable` marks attributes intended for product discovery and `is_variant_axis` marks attributes intended to participate in variant selection in P04.

Attribute value slugs are unique within each attribute at database level.

## Category hierarchy

A category may have one parent. Model validation rejects self-parenting and cyclic ancestry. Parent deletion is protected so catalog structure cannot be silently damaged by deleting a referenced parent.

## Media boundary

Image/logo/swatch fields are URL references in P02. P05 will replace the underlying management mechanism with the dedicated media pipeline without requiring Lovable to own media state.

## Deferred scope

Product relations belong to P03. Variant combinations and SKU-level option selection belong to P04. Search indexing and advanced faceting belong to P06. SEO metadata belongs to P15.
