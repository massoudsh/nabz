from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_campaign_simulation_projects_profit_and_holds_do_not_disturb():
    response = client.post(
        "/demo/simulations",
        json={
            "customer_ids": ["demo_maryam", "demo_niloofar", "demo_roya"],
            "gross_margin_rate": 0.35,
            "minimum_expected_profit": 1000,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["customer_count"] == 3
    assert body["eligible_count"] == 2
    assert body["held_count"] == 1
    assert body["projected_profit"] > 0
    rooya = next(item for item in body["items"] if item["customer_id"] == "demo_roya")
    assert rooya["is_profitable"] is False
    assert rooya["action"] == "do_not_disturb"


def test_campaign_simulation_holds_unprofitable_incentive():
    response = client.post(
        "/demo/simulations",
        json={
            "customer_ids": ["demo_maryam"],
            "gross_margin_rate": 0.1,
            "free_shipping_cost": 300000,
            "minimum_expected_profit": 0,
        },
    )

    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["is_profitable"] is False
    assert "حداقل سود" in item["guardrail_reason"]
