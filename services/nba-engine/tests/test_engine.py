"""تست‌های موتور تصمیم‌ساز — بر اساس پرسوناهای docs/PRD.md بخش ۴."""

import json
import pathlib

import pytest

from app.engine import decide
from app.models import Action, Customer

EXAMPLES_PATH = pathlib.Path(__file__).resolve().parent.parent / "examples" / "sample_customers.json"


def load_persona(key: str) -> Customer:
    data = json.loads(EXAMPLES_PATH.read_text(encoding="utf-8"))
    return Customer(**data[key])


@pytest.mark.parametrize(
    "persona_key,expected_action",
    [
        ("reminder_only", Action.REMINDER),
        ("free_shipping_sensitive", Action.FREE_SHIPPING),
        ("no_discount_needed", Action.VIP_NO_DISCOUNT),
        ("needs_bnpl", Action.BNPL_OFFER),
        ("do_not_overmessage", Action.DO_NOT_DISTURB),
        ("urgent_churn_risk", Action.WIN_BACK),
    ],
)
def test_persona_gets_expected_action(persona_key: str, expected_action: Action):
    customer = load_persona(persona_key)
    decision = decide(customer)
    assert decision.recommended_action == expected_action
    assert decision.customer_id == customer.customer_id
    assert 0 <= decision.confidence <= 1
    assert len(decision.reasoning) >= 1


def test_do_not_disturb_has_empty_message():
    customer = load_persona("do_not_overmessage")
    decision = decide(customer)
    assert decision.message_fa == ""
    assert decision.do_not_disturb is True


def test_opted_out_always_wins():
    customer = load_persona("urgent_churn_risk")
    customer.opted_out = True
    decision = decide(customer)
    assert decision.recommended_action == Action.DO_NOT_DISTURB


def test_message_contains_customer_name():
    customer = load_persona("free_shipping_sensitive")
    decision = decide(customer)
    assert customer.name in decision.message_fa


def test_sms_channel_has_no_common_emoji():
    customer = load_persona("urgent_churn_risk")
    decision = decide(customer)
    assert decision.channel.value == "sms"
    for emoji in ["🌸", "🙌", "😊", "✨"]:
        assert emoji not in decision.message_fa
