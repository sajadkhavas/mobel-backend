from django.urls import reverse


def test_health_endpoint(client):
    response = client.get(reverse("health"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "mobel-backend"}


def test_readiness_endpoint(client, db):
    response = client.get(reverse("system-ready"))
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["checks"] == {"database": True, "cache": True}
