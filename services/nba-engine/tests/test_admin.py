"""تست پنل مدیریتی — لاگ تصمیم + تایید/رد (issue #3)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CUSTOMER_PAYLOAD = {
    "customer_id": "c_admin_flow",
    "name": "نگار",
    "orders": [],
    "cart": {"status": "none"},
}


def test_decide_logs_decision_visible_in_admin_dashboard():
    decide_response = client.post("/decide", json=CUSTOMER_PAYLOAD)
    assert decide_response.status_code == 200

    dashboard = client.get("/admin")
    assert dashboard.status_code == 200
    assert "c_admin_flow" in dashboard.text
    assert "در انتظار" in dashboard.text  # فیلتر pending در ناوبری


def test_approve_decision_changes_status():
    client.post("/decide", json={**CUSTOMER_PAYLOAD, "customer_id": "c_admin_approve"})
    pending = client.get("/admin?status=pending").text
    assert "c_admin_approve" in pending

    # decision_id را از دیتابیس داخلی می‌خوانیم چون در HTML صریحاً چاپ نشده
    from app import decision_store

    match = next(
        d for d in decision_store.list_decisions(status="pending") if d.customer_id == "c_admin_approve"
    )
    approve_response = client.post(f"/admin/decisions/{match.id}/approve")
    assert approve_response.status_code in (200, 303)

    updated = next(
        d for d in decision_store.list_decisions() if d.id == match.id
    )
    assert updated.status == "approved"


def test_approve_unknown_decision_returns_404():
    response = client.post("/admin/decisions/does-not-exist/approve")
    assert response.status_code == 404
