"""تست‌های موتور تصمیم‌ساز — بر اساس پرسوناهای docs/PRD.md بخش ۴."""

import json
import pathlib
from datetime import date, datetime, timedelta

import pytest

from app.engine import decide
from app.models import Action, Customer

EXAMPLES_PATH = pathlib.Path(__file__).resolve().parent.parent / "examples" / "sample_customers.json"

# پرسوناهای examples/sample_customers.json با تاریخ‌های مطلق نوشته شده‌اند، طوری‌که
# نسبت به این «امروز» فرضی معنا دارند (مثلاً «سبد ۲ روز پیش رها شده»). چون زمان واقعی
# اجرای تست جلو می‌رود، تاریخ‌ها را هر بار به همان فاصله‌ی نسبی از «امروز واقعی» جابه‌جا
# می‌کنیم تا تست‌ها به تاریخ اجرا وابسته و flaky نشوند.
FIXTURE_ANCHOR = date(2026, 7, 25)
_DATE_KEYS = {"ordered_at", "joined_at"}
_DATETIME_KEYS = {"updated_at", "occurred_at", "last_story_reaction_at"}


def _shift(node, delta: timedelta):
    if isinstance(node, dict):
        shifted = {}
        for key, value in node.items():
            if key in _DATE_KEYS and isinstance(value, str):
                shifted[key] = (date.fromisoformat(value) + delta).isoformat()
            elif key in _DATETIME_KEYS and isinstance(value, str):
                dt_value = datetime.fromisoformat(value.replace("Z", "+00:00")) + delta
                shifted[key] = dt_value.isoformat().replace("+00:00", "Z")
            else:
                shifted[key] = _shift(value, delta)
        return shifted
    if isinstance(node, list):
        return [_shift(item, delta) for item in node]
    return node


def load_persona(key: str) -> Customer:
    data = json.loads(EXAMPLES_PATH.read_text(encoding="utf-8"))
    delta = date.today() - FIXTURE_ANCHOR
    return Customer(**_shift(data[key], delta))


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
