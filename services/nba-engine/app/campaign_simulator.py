from __future__ import annotations

from app.demo import customer_by_id
from app.engine import decide
from app.models import (
    Action,
    CampaignSimulation,
    CampaignSimulationItem,
    CampaignSimulationRequest,
    CartStatus,
)


def _basket_value(customer) -> float:
    if customer.cart.status != CartStatus.NONE and customer.cart.items_value > 0:
        return customer.cart.items_value
    if customer.orders:
        return sum(order.amount for order in customer.orders) / len(customer.orders)
    return customer.store_avg_cart_value


def _incentive_cost(action: Action, basket_value: float, request: CampaignSimulationRequest) -> float:
    if action == Action.FREE_SHIPPING:
        return request.free_shipping_cost
    if action == Action.DISCOUNT_PERCENT:
        return basket_value * request.discount_rate
    if action == Action.CASHBACK:
        return basket_value * request.cashback_rate
    if action == Action.WIN_BACK:
        return basket_value * request.win_back_rate
    return 0.0


def simulate_demo_campaign(request: CampaignSimulationRequest) -> CampaignSimulation:
    items: list[CampaignSimulationItem] = []

    for customer_id in request.customer_ids:
        customer = customer_by_id(customer_id)
        if customer is None:
            continue
        decision = decide(customer)
        basket_value = _basket_value(customer)
        incentive_cost = _incentive_cost(decision.recommended_action, basket_value, request)
        expected_revenue = basket_value * decision.confidence
        expected_profit = expected_revenue * request.gross_margin_rate - incentive_cost
        is_held = decision.do_not_disturb or expected_profit < request.minimum_expected_profit
        if decision.do_not_disturb:
            reason = "مشتری نباید پیام جدیدی دریافت کند؛ سقف تماس یا رضایت او رعایت می‌شود."
        elif expected_profit < request.minimum_expected_profit:
            reason = "پیشنهاد با حداقل سود مورد انتظار کمپین هم‌خوان نیست و نگه داشته می‌شود."
        else:
            reason = "پیشنهاد از محافظ سودآوری عبور کرده و برای اجرا مناسب است."
        items.append(
            CampaignSimulationItem(
                customer_id=customer.customer_id,
                customer_name=customer.name,
                action=decision.recommended_action,
                channel=decision.channel,
                basket_value=round(basket_value),
                confidence=decision.confidence,
                incentive_cost=round(incentive_cost),
                expected_revenue=round(expected_revenue),
                expected_profit=round(expected_profit),
                is_profitable=not is_held,
                guardrail_reason=reason,
            )
        )

    eligible = [item for item in items if item.is_profitable]
    protected_margin = sum(item.incentive_cost for item in items if not item.is_profitable)
    return CampaignSimulation(
        customer_count=len(items),
        eligible_count=len(eligible),
        held_count=len(items) - len(eligible),
        projected_revenue=round(sum(item.expected_revenue for item in eligible)),
        incentive_cost=round(sum(item.incentive_cost for item in eligible)),
        projected_profit=round(sum(item.expected_profit for item in eligible)),
        protected_margin=round(protected_margin),
        items=items,
    )
