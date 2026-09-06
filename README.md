# Mobel Backend

Production-oriented backend for a configurable furniture commerce platform.

## Stack

- Python 3.14
- Django 5.2 LTS
- Django REST Framework 3.18
- PostgreSQL in production
- Redis for shared cache/runtime services

## Core architecture rule

The backend is authoritative for business data, merchant-manageable storefront content, commerce configuration, SEO metadata, and feature flags. The Lovable/React frontend owns presentation and interaction, not merchant state.

See `docs/ARCHITECTURE.md`.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Environment variables are intentionally explicit; Django does not automatically read `.env`. Export them in the shell/container runtime or load them through the deployment environment.

## Quality gates

```bash
ruff check .
ruff format --check .
python manage.py check --settings=config.settings.test
pytest
```

## API

Versioned root: `/api/v1/`

System endpoints:

- `GET /health/`
- `GET /api/v1/system/ready/`

## Delivery workflow

Every phase uses a dedicated branch and pull request. A phase is only considered complete after its tests and CI gates pass and it is merged into `main`.
