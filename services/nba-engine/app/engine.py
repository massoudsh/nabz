"""Next-Best-Action decision engine — پیاده‌سازی منطق docs/ARCHITECTURE.md بخش ۳ و ۴."""

from __future__ import annotations

from datetime import date, datetime, timezone
from statistics import mean

from app import feedback_store
from app.catalog import ACTION_METADATA
from app.channels import render_message
from app.models import (
    AbandonStage,
    Action,
    CartStatus,
    Channel,
    ConversationIntent,
    Customer,
    Decision,
)

# حداکثر میزان جابه‌جایی confidence بر اساس بازخورد واقعی (فاز ۲، issue #5).
_ADAPTIVE_ADJUSTMENT_CAP = 0.15


def _adaptive_adjustment(action: Action) -> float:
    """تنظیم confidence بر اساس نرخ خرید واقعیِ ثبت‌شده برای این اقدام.

    docs/ARCHITECTURE.md بخش ۵: به‌جای وزن ثابت، از CampaignHistory واقعی
    استفاده می‌شود. اگر نمونه‌ی کافی نباشد (feedback_store برمی‌گرداند None)
    بدون تغییر باقی می‌ماند تا رفتار MVP حفظ شود.
    """
    rate = feedback_store.purchase_rate_for_action(action)
    if rate is None:
        return 0.0
    return _clamp((rate - 0.5) * 2 * _ADAPTIVE_ADJUSTMENT_CAP, -_ADAPTIVE_ADJUSTMENT_CAP, _ADAPTIVE_ADJUSTMENT_CAP)


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _today() -> date:
    return date.today()


def compute_signals(customer: Customer) -> dict[str, float]:
    """محاسبه‌ی امتیاز هر سیگنال بین ۰ و ۱ — docs/ARCHITECTURE.md بخش ۳."""

    orders = sorted(customer.orders, key=lambda o: o.ordered_at)

    # frequency_score
    frequency_score = _clamp(len(orders) / 8.0)

    # discount_sensitivity
    if orders:
        discount_sensitivity = sum(1 for o in orders if o.used_discount_code) / len(orders)
    else:
        discount_sensitivity = 0.5  # بدون سابقه → خنثی

    # churn_risk (بر اساس recency نسبت به بازه‌ی معمول خرید مشتری)
    if not orders:
        churn_risk = 0.4  # مشتری جدید بدون سابقه، ریسک نامشخص
    else:
        days_since_last = (_today() - orders[-1].ordered_at).days
        if len(orders) >= 2:
            gaps = [
                (orders[i + 1].ordered_at - orders[i].ordered_at).days
                for i in range(len(orders) - 1)
            ]
            avg_gap = mean(gaps) if mean(gaps) > 0 else 30
        else:
            avg_gap = 30  # فرض بازه‌ی معمول ماهانه برای مشتری تک‌خرید
        churn_risk = _clamp(days_since_last / (avg_gap * 1.5))

    # shipping_sensitivity (نسبت رهاشدن سبد در مرحله دیدن هزینه ارسال)
    history = list(customer.past_cart_abandon_stage_history)
    if customer.cart.status == CartStatus.ABANDONED:
        history = history + [customer.cart.abandon_stage]
    if history:
        shipping_sensitivity = sum(
            1 for s in history if s == AbandonStage.SHIPPING_COST_SEEN
        ) / len(history)
    else:
        shipping_sensitivity = 0.3  # خنثی، بدون داده کافی

    # cart_urgency
    if customer.cart.status == CartStatus.ABANDONED:
        if customer.cart.updated_at:
            hours_since = (_now() - customer.cart.updated_at).total_seconds() / 3600
        else:
            hours_since = 24
        recency_component = _clamp(1 - hours_since / 72)
        value_component = _clamp(
            customer.cart.items_value / max(customer.store_avg_cart_value * 2, 1)
        )
        cart_urgency = _clamp(0.6 * recency_component + 0.4 * value_component)
    else:
        cart_urgency = 0.0

    # conversation_intent_signal
    conversation_intent_signal = 0.0
    for conv in customer.recent_conversations:
        hours_since = (_now() - conv.occurred_at).total_seconds() / 3600
        if conv.intent in (ConversationIntent.PRICE_QUESTION, ConversationIntent.INTEREST):
            if hours_since <= 48:
                conversation_intent_signal = max(
                    conversation_intent_signal, _clamp(1 - hours_since / 48)
                )

    # contact_budget_remaining (نرمال‌نشده، عدد صحیح باقی‌مانده)
    contact_budget_remaining = customer.max_messages_per_week - customer.messages_sent_last_7_days

    return {
        "frequency_score": round(frequency_score, 3),
        "discount_sensitivity": round(discount_sensitivity, 3),
        "churn_risk": round(churn_risk, 3),
        "shipping_sensitivity": round(shipping_sensitivity, 3),
        "cart_urgency": round(cart_urgency, 3),
        "conversation_intent_signal": round(conversation_intent_signal, 3),
        "contact_budget_remaining": float(contact_budget_remaining),
    }


def decide(customer: Customer) -> Decision:
    """اجرای قوانین اولویت‌دار — docs/ARCHITECTURE.md بخش ۴."""

    signals = compute_signals(customer)
    reasoning: list[str] = []

    def finalize(action: Action, channel: Channel, confidence: float) -> Decision:
        meta = ACTION_METADATA[action]
        if action != Action.DO_NOT_DISTURB:
            adjustment = _adaptive_adjustment(action)
            if adjustment != 0.0:
                reasoning.append(
                    f"امتیاز بر اساس نرخ خرید واقعی این اقدام در بازخوردهای قبلی تنظیم شد ({adjustment:+.2f})"
                )
            confidence = confidence + adjustment
        return Decision(
            customer_id=customer.customer_id,
            recommended_action=action,
            channel=channel,
            urgency=meta["urgency"],
            message_fa=render_message(action, channel, customer.name),
            reasoning=reasoning,
            confidence=round(_clamp(confidence), 2),
            do_not_disturb=(action == Action.DO_NOT_DISTURB),
            signals=signals,
        )

    # قانون ۱: opt-out یا اتمام سقف فرکانس
    if customer.opted_out:
        reasoning.append("مشتری درخواست عدم تماس داده (opted_out=true)")
        return finalize(Action.DO_NOT_DISTURB, customer.preferred_channel, 1.0)
    if signals["contact_budget_remaining"] <= 0:
        reasoning.append(
            f"سقف پیام هفتگی پر شده ({customer.messages_sent_last_7_days}/{customer.max_messages_per_week})"
        )
        return finalize(Action.DO_NOT_DISTURB, customer.preferred_channel, 0.9)

    # قانون ۲: ریسک ریزش بالا
    if signals["churn_risk"] >= 0.7:
        reasoning.append(f"ریسک ریزش بالا (churn_risk={signals['churn_risk']})")
        return finalize(Action.WIN_BACK, customer.preferred_channel, 0.6 + 0.4 * signals["churn_risk"])

    # قانون ۳: سبد رهاشده در مرحله پرداخت با ارزش بالا → BNPL
    if (
        customer.cart.status == CartStatus.ABANDONED
        and customer.cart.abandon_stage == AbandonStage.PAYMENT_PAGE
        and customer.cart.items_value > customer.store_avg_cart_value
    ):
        reasoning.append("سبد در مرحله پرداخت رها شده و ارزش آن بالاتر از میانگین فروشگاه است")
        return finalize(Action.BNPL_OFFER, customer.preferred_channel, 0.55 + 0.4 * signals["cart_urgency"])

    # قانون ۴: سبد رهاشده هنگام دیدن هزینه ارسال + حساسیت بالا
    if (
        customer.cart.status == CartStatus.ABANDONED
        and customer.cart.abandon_stage == AbandonStage.SHIPPING_COST_SEEN
        and signals["shipping_sensitivity"] >= 0.5
    ):
        reasoning.append(
            f"سبد هنگام دیدن هزینه ارسال رها شده و حساسیت به ارسال بالاست ({signals['shipping_sensitivity']})"
        )
        return finalize(Action.FREE_SHIPPING, customer.preferred_channel, 0.5 + 0.4 * signals["shipping_sensitivity"])

    # قانون ۵: مشتری وفادار بدون نیاز به تخفیف
    if signals["discount_sensitivity"] <= 0.15 and signals["frequency_score"] >= 0.5:
        reasoning.append(
            f"سابقه‌ی خرید بدون تخفیف (discount_sensitivity={signals['discount_sensitivity']}) و خرید مکرر"
        )
        return finalize(Action.VIP_NO_DISCOUNT, customer.preferred_channel, 0.5 + 0.4 * signals["frequency_score"])

    # قانون ۶: سوال قیمت اخیر بدون خرید
    if signals["conversation_intent_signal"] > 0:
        reasoning.append("سوال قیمت/علاقه در مکالمه اخیر بدون خرید بعدی")
        return finalize(
            Action.DISCOUNT_PERCENT, customer.preferred_channel, 0.5 + 0.4 * signals["conversation_intent_signal"]
        )

    # قانون ۷: خرید مکرر با حساسیت متوسط به تخفیف → کش‌بک
    if signals["frequency_score"] >= 0.6 and 0.15 < signals["discount_sensitivity"] < 0.6:
        reasoning.append("مشتری تکرارشونده با حساسیت متوسط به تخفیف")
        return finalize(Action.CASHBACK, customer.preferred_channel, 0.5 + 0.3 * signals["frequency_score"])

    # قانون ۸: سبد فعال با چند دسته مرتبط
    if customer.cart.status == CartStatus.ACTIVE and customer.cart.distinct_categories >= 2:
        reasoning.append("سبد فعال شامل چند دسته‌ی مرتبط است")
        return finalize(Action.BUNDLE_OFFER, customer.preferred_channel, 0.55)

    # پیش‌فرض: یادآوری ساده
    reasoning.append("هیچ سیگنال قوی‌ای یافت نشد؛ یادآوری ساده مناسب‌ترین گزینه است")
    return finalize(Action.REMINDER, customer.preferred_channel, 0.4)
