from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


def health(request):
    return JsonResponse({"status": "ok", "service": "mobel-backend"})


@api_view(["GET"])
def readiness(request):
    checks = {"database": False, "cache": False}

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        checks["database"] = cursor.fetchone() == (1,)

    cache_key = "system-readiness"
    cache.set(cache_key, "ok", timeout=5)
    checks["cache"] = cache.get(cache_key) == "ok"

    ready = all(checks.values())
    return Response(
        {"status": "ready" if ready else "not_ready", "checks": checks},
        status=200 if ready else 503,
    )
