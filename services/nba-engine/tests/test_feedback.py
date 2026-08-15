"""تست endpoint بازخورد — docs/ARCHITECTURE.md بخش ۲ (CampaignHistory)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_record_and_fetch_feedback():
    payload = {
        "customer_id": "c_feedback_test",
        "action": "free_shipping",
        "channel": "whatsapp",
        "opened": True,
        "purchased": True,
    }
    post_response = client.post("/feedback", json=payload)
    assert post_response.status_code == 200
    assert post_response.json()["customer_id"] == "c_feedback_test"

    get_response = client.get("/feedback/c_feedback_test")
    assert get_response.status_code == 200
    history = get_response.json()
    assert len(history) == 1
    assert history[0]["purchased"] is True


def test_feedback_not_found_returns_404():
    response = client.get("/feedback/c_never_recorded")
    assert response.status_code == 404
