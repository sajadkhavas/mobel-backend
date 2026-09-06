# Mobel Backend Architecture

## Backend-authoritative rule

Any frontend value that is business data, merchant-manageable content, commerce configuration, SEO metadata, or a feature switch must be stored and managed by the backend and delivered through versioned APIs.

Frontend code owns presentation details such as responsive layout, spacing, animation, interaction implementation, and accessibility behavior. It must not become the source of truth for merchant data.

## Boundaries

### Backend-owned
- store identity and contact data
- navigation and footer content
- hero, banners, homepage section content and ordering
- catalog, variants, prices, inventory, delivery and payment state
- customer, cart, order and review data
- blog, FAQ, policies and editable pages
- SEO fields and redirects
- feature flags and merchant settings

### Frontend-owned
- component composition
- responsive breakpoints
- spacing and visual styling
- animations and transitions
- interaction mechanics
- accessibility implementation

## API policy

Public storefront APIs are versioned under `/api/v1/`.

Backend responses are the source of truth. Pricing and order totals are always calculated and validated server-side.

## Environment policy

- development: developer-friendly settings; SQLite is permitted for bootstrapping
- test: isolated in-memory database unless an integration test requires PostgreSQL
- production: PostgreSQL is mandatory; a non-default secret key is mandatory

Redis is used when configured and is validated by production CI.

## P00 system endpoints

- `GET /health/` — process liveness only
- `GET /api/v1/system/ready/` — verifies database and cache readiness
