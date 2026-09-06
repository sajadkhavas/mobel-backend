# Mobel Backend

Backend for a production-oriented furniture commerce platform.

## Architecture principle

The backend is authoritative for all business data, storefront content, commerce configuration, SEO metadata, and feature flags. The frontend is responsible for presentation and interaction only.

## Planned stack

- Python 3.14
- Django 5.2 LTS
- Django REST Framework 3.18
- PostgreSQL
- Redis

## API

Versioned API root: `/api/v1/`

Health endpoints:

- `/health/`
- `/api/v1/system/ready/`

## Delivery workflow

Each implementation phase is developed on a dedicated branch, validated by CI, reviewed through a pull request, and merged only after its gates pass.
