from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_storefront_and_channel_ingestion_builds_customer_snapshot_and_decision():
    order_response = client.post(
        "/integrations/storefront/orders",
        json={
            "provider": "woocommerce",
            "customer_id": "c_integrated",
            "customer_name": "مریم",
            "order_id": "ord_1",
            "amount": 420000,
            "used_discount_code": False,
            "ordered_at": "2026-09-01",
        },
    )
    assert order_response.status_code == 200

    cart_response = client.post(
        "/integrations/storefront/cart",
        json={
            "customer_id": "c_integrated",
            "customer_name": "مریم",
            "status": "abandoned",
            "items_value": 1200000,
            "abandon_stage": "payment_page",
            "distinct_categories": 2,
        },
    )
    assert cart_response.status_code == 200

    conversation_response = client.post(
        "/integrations/conversations",
        json={
            "provider": "whatsapp_business",
            "customer_id": "c_integrated",
            "customer_name": "مریم",
            "channel": "whatsapp",
            "text": "قیمت این مدل چقدر است؟",
            "intent": "price_question",
        },
    )
    assert conversation_response.status_code == 200

    snapshot_response = client.get("/integrations/customers/c_integrated")
    assert snapshot_response.status_code == 200
    snapshot = snapshot_response.json()
    assert snapshot["customer"]["name"] == "مریم"
    assert snapshot["order_count"] == 1
    assert snapshot["conversation_count"] == 1
    assert snapshot["customer"]["cart"]["status"] == "abandoned"

    decision_response = client.post("/integrations/customers/c_integrated/decide")
    assert decision_response.status_code == 200
    assert decision_response.json()["customer_id"] == "c_integrated"


def test_missing_integrated_customer_returns_404():
    assert client.get("/integrations/customers/c_missing").status_code == 404
    assert client.post("/integrations/customers/c_missing/decide").status_code == 404


def test_campaign_report_counts_decisions_and_feedback():
    client.post(
        "/feedback",
        json={
            "customer_id": "c_report",
            "action": "reminder",
            "channel": "sms",
            "opened": True,
            "purchased": False,
        },
    )

    response = client.get("/reports/campaigns")
    assert response.status_code == 200
    body = response.json()
    assert body["feedback_count"] >= 1
    assert body["opened_count"] >= 1
    assert 0 <= body["purchase_rate"] <= 1
    assert body["total_decisions"] >= 0
