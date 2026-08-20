"""تست endpoint دسته‌ای (issue #8) و احراز هویت API key (issue #7)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CUSTOMER_PAYLOAD = {
    "customer_id": "c_batch_1",
    "name": "سارا",
    "orders": [],
    "cart": {"status": "none"},
}


def test_decide_batch_returns_decision_per_customer():
    payload = [CUSTOMER_PAYLOAD, {**CUSTOMER_PAYLOAD, "customer_id": "c_batch_2"}]
    response = client.post("/decide/batch", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {d["customer_id"] for d in body} == {"c_batch_1", "c_batch_2"}


def test_decide_without_api_key_when_none_configured_is_allowed():
    response = client.post("/decide", json=CUSTOMER_PAYLOAD)
    assert response.status_code == 200


def test_decide_requires_api_key_when_configured(monkeypatch):
    monkeypatch.setenv("NBA_API_KEYS", "secret-key-1,secret-key-2")

    rejected = client.post("/decide", json=CUSTOMER_PAYLOAD)
    assert rejected.status_code == 401

    accepted = client.post(
        "/decide", json=CUSTOMER_PAYLOAD, headers={"X-API-Key": "secret-key-2"}
    )
    assert accepted.status_code == 200


def test_health_never_requires_api_key(monkeypatch):
    monkeypatch.setenv("NBA_API_KEYS", "secret-key-1")
    assert client.get("/health").status_code == 200


def test_admin_requires_api_key_via_query_param(monkeypatch):
    monkeypatch.setenv("NBA_API_KEYS", "secret-key-1")

    rejected = client.get("/admin")
    assert rejected.status_code == 401

    accepted = client.get("/admin?api_key=secret-key-1")
    assert accepted.status_code == 200
    assert "پنل مدیریتی" in accepted.text
