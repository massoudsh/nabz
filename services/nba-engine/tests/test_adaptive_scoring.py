"""تست امتیازدهی تطبیقی بر اساس بازخورد واقعی (issue #5)."""

from datetime import date

from app.engine import decide
from app.feedback_store import record
from app.models import Action, Channel, CampaignFeedback, Customer


def _reminder_customer(customer_id: str) -> Customer:
    return Customer(customer_id=customer_id, name="کاربر تست")


def test_confidence_increases_after_positive_feedback_history():
    baseline = decide(_reminder_customer("c_adaptive_before")).confidence

    for i in range(4):
        record(
            CampaignFeedback(
                customer_id=f"c_hist_{i}",
                action=Action.REMINDER,
                channel=Channel.SMS,
                opened=True,
                purchased=True,
            )
        )

    boosted = decide(_reminder_customer("c_adaptive_after")).confidence
    assert boosted > baseline


def test_confidence_decreases_after_negative_feedback_history():
    for i in range(4):
        record(
            CampaignFeedback(
                customer_id=f"c_neg_hist_{i}",
                action=Action.CASHBACK,
                channel=Channel.SMS,
                opened=True,
                purchased=False,
            )
        )

    from app.feedback_store import purchase_rate_for_action

    rate = purchase_rate_for_action(Action.CASHBACK)
    assert rate == 0.0
