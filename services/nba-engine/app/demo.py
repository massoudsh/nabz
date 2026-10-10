from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from app.engine import decide
from app.models import (
    AbandonStage,
    CartEvent,
    CartStatus,
    Channel,
    ConversationEvent,
    ConversationIntent,
    Customer,
    Decision,
    DemoOverview,
    Order,
)


def customers() -> list[Customer]:
    today = date.today()
    now = datetime.now(timezone.utc)
    return [
        Customer(
            customer_id="demo_maryam",
            name="مریم احمدی",
            preferred_channel=Channel.WHATSAPP,
            orders=[
                Order(order_id="m-1", amount=340000, ordered_at=today - timedelta(days=55)),
                Order(order_id="m-2", amount=410000, ordered_at=today - timedelta(days=28)),
            ],
            cart=CartEvent(
                status=CartStatus.ABANDONED,
                items_value=520000,
                abandon_stage=AbandonStage.SHIPPING_COST_SEEN,
                updated_at=now - timedelta(hours=7),
            ),
            past_cart_abandon_stage_history=[AbandonStage.SHIPPING_COST_SEEN],
        ),
        Customer(
            customer_id="demo_niloofar",
            name="نیلوفر رضایی",
            preferred_channel=Channel.INSTAGRAM_DM,
            orders=[Order(order_id="n-1", amount=280000, ordered_at=today - timedelta(days=18))],
            cart=CartEvent(
                status=CartStatus.ABANDONED,
                items_value=1450000,
                abandon_stage=AbandonStage.PAYMENT_PAGE,
                updated_at=now - timedelta(hours=2),
            ),
        ),
        Customer(
            customer_id="demo_ava",
            name="آوا کریمی",
            preferred_channel=Channel.INSTAGRAM_DM,
            recent_conversations=[
                ConversationEvent(
                    channel=Channel.INSTAGRAM_DM,
                    text="قیمت این مدل چقدر است؟",
                    intent=ConversationIntent.PRICE_QUESTION,
                    occurred_at=now - timedelta(hours=4),
                )
            ],
        ),
        Customer(
            customer_id="demo_leila",
            name="لیلا محمدی",
            preferred_channel=Channel.WHATSAPP,
            orders=[
                Order(order_id=f"l-{index}", amount=370000 + index * 10000, ordered_at=today - timedelta(days=7 * (8 - index)))
                for index in range(8)
            ],
        ),
        Customer(
            customer_id="demo_sahar",
            name="سحر اکبری",
            preferred_channel=Channel.SMS,
            orders=[
                Order(order_id="s-1", amount=420000, ordered_at=today - timedelta(days=150)),
                Order(order_id="s-2", amount=390000, ordered_at=today - timedelta(days=110)),
            ],
        ),
        Customer(
            customer_id="demo_roya",
            name="رویا حسینی",
            preferred_channel=Channel.WHATSAPP,
            max_messages_per_week=2,
            messages_sent_last_7_days=2,
        ),
    ]


def customer_by_id(customer_id: str) -> Customer | None:
    return next((customer for customer in customers() if customer.customer_id == customer_id), None)


def decisions() -> list[Decision]:
    return [decide(customer) for customer in customers()]


def overview() -> DemoOverview:
    results = decisions()
    counts: dict[str, int] = {}
    for result in results:
        action = result.recommended_action.value
        counts[action] = counts.get(action, 0) + 1
    return DemoOverview(customers=customers(), decisions=results, action_counts=counts)
