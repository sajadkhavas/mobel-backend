import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False

if SECRET_KEY == "unsafe-development-key":  # noqa: F405
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production")
if os.getenv("DB_ENGINE") != "postgresql":
    raise ImproperlyConfigured("Production requires DB_ENGINE=postgresql")
if not ALLOWED_HOSTS:  # noqa: F405
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must be set in production")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
