"""Pydantic schemas for the Nabz Next-Best-Action engine."""

from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Channel(str, Enum):
    INSTAGRAM_DM = "instagram_dm"
    WHATSAPP = "whatsapp"
    SMS = "sms"


class AbandonStage(str, Enum):
    NONE = "none"
    SHIPPING_COST_SEEN = "shipping_cost_seen"
    PAYMENT_PAGE = "payment_page"


class CartStatus(str, Enum):
    ABANDONED = "abandoned"
    ACTIVE = "active"
    COMPLETED = "completed"
    NONE = "none"


class ConversationIntent(str, Enum):
    PRICE_QUESTION = "price_question"
    COMPLAINT = "complaint"
    INTEREST = "interest"
    NONE = "none"


class Action(str, Enum):
    REMINDER = "reminder"
    FREE_SHIPPING = "free_shipping"
    DISCOUNT_PERCENT = "discount_percent"
    CASHBACK = "cashback"
    BNPL_OFFER = "bnpl_offer"
    BUNDLE_OFFER = "bundle_offer"
    VIP_NO_DISCOUNT = "vip_no_discount"
    WIN_BACK = "win_back"
    DO_NOT_DISTURB = "do_not_disturb"


class Order(BaseModel):
    order_id: str
    amount: float = Field(..., ge=0, description="مبلغ سفارش به تومان")
    used_discount_code: bool = False
    ordered_at: date


class CartEvent(BaseModel):
    status: CartStatus = CartStatus.NONE
    items_value: float = Field(0, ge=0)
    abandon_stage: AbandonStage = AbandonStage.NONE
    updated_at: Optional[datetime] = None
    distinct_categories: int = Field(0, ge=0, description="تعداد دسته‌های متفاوت آیتم‌های سبد فعلی")


class ConversationEvent(BaseModel):
    channel: Channel
    text: str = ""
    intent: ConversationIntent = ConversationIntent.NONE
    occurred_at: datetime


class Customer(BaseModel):
    customer_id: str
    name: str = "مشتری"
    preferred_channel: Channel = Channel.INSTAGRAM_DM
    opted_out: bool = False
    max_messages_per_week: int = Field(3, ge=0)
    messages_sent_last_7_days: int = Field(0, ge=0)
    joined_at: Optional[date] = None

    orders: list[Order] = Field(default_factory=list)
    cart: CartEvent = Field(default_factory=CartEvent)
    recent_conversations: list[ConversationEvent] = Field(default_factory=list)
    last_story_reaction_at: Optional[datetime] = None
    past_cart_abandon_stage_history: list[AbandonStage] = Field(
        default_factory=list, description="سابقه‌ی مرحله‌ی رهاشدن سبدهای قبلی (اختیاری)"
    )

    # میانگین ارزش سبد فروشگاه، برای مقایسه نسبی سبد این مشتری (اختیاری، پیش‌فرض معقول)
    store_avg_cart_value: float = Field(300000, ge=0)


class Decision(BaseModel):
    customer_id: str
    recommended_action: Action
    channel: Channel
    urgency: str  # low | medium | high
    message_fa: str
    reasoning: list[str]
    confidence: float = Field(..., ge=0, le=1)
    do_not_disturb: bool = False
    signals: dict[str, float] = Field(default_factory=dict)


class CampaignFeedback(BaseModel):
    """نتیجه‌ی واقعی یک اقدام پیشنهادی — docs/ARCHITECTURE.md بخش ۲ (CampaignHistory).

    فاز MVP فقط این بازخورد را ذخیره می‌کند؛ استفاده در امتیازدهی تطبیقی، فاز ۲ است.
    """

    customer_id: str
    action: Action
    channel: Channel
    opened: bool = False
    purchased: bool = False
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
