from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_demo_overview_exposes_mock_customers_and_engine_results():
    response = client.get("/demo/overview")

    assert response.status_code == 200
    body = response.json()
    assert len(body["customers"]) == 6
    assert len(body["decisions"]) == 6
    assert body["action_counts"]["free_shipping"] == 1
    assert body["action_counts"]["bnpl_offer"] == 1
    assert body["action_counts"]["do_not_disturb"] == 1


def test_demo_customer_decision_uses_engine_and_logs_result():
    response = client.post("/demo/customers/demo_maryam/decide")

    assert response.status_code == 200
    body = response.json()
    assert body["recommended_action"] == "free_shipping"
    assert body["channel"] == "whatsapp"
    assert body["reasoning"]


def test_unknown_demo_customer_returns_404():
    response = client.post("/demo/customers/unknown/decide")

    assert response.status_code == 404
