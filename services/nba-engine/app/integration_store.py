from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base, SessionLocal
from app.models import (
    CartEvent,
    ConversationEvent,
    ConversationIngest,
    Customer,
    CustomerSnapshot,
    Order,
    StorefrontCartIngest,
    StorefrontOrderIngest,
)


class CustomerProfileRecord(Base):
    __tablename__ = "customer_profiles"

    customer_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="مشتری")
    preferred_channel: Mapped[str] = mapped_column(String, default="instagram_dm")
    opted_out: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class IngestedOrderRecord(Base):
    __tablename__ = "ingested_orders"

    order_id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[float] = mapped_column(Float)
    used_discount_code: Mapped[bool] = mapped_column(Boolean, default=False)
    ordered_at: Mapped[date] = mapped_column(Date)
    provider: Mapped[str] = mapped_column(String)


class IngestedCartRecord(Base):
    __tablename__ = "ingested_carts"

    customer_id: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[str] = mapped_column(String)
    items_value: Mapped[float] = mapped_column(Float)
    abandon_stage: Mapped[str] = mapped_column(String)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    distinct_categories: Mapped[int] = mapped_column(Integer, default=0)
    provider: Mapped[str] = mapped_column(String)


class IngestedConversationRecord(Base):
    __tablename__ = "ingested_conversations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(String, index=True)
    provider: Mapped[str] = mapped_column(String)
    channel: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    intent: Mapped[str] = mapped_column(String)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _upsert_profile(customer_id: str, name: str, preferred_channel: str, opted_out: bool, updated_at: datetime) -> None:
    with SessionLocal() as session:
        profile = session.get(CustomerProfileRecord, customer_id)
        if profile is None:
            session.add(
                CustomerProfileRecord(
                    customer_id=customer_id,
                    name=name,
                    preferred_channel=preferred_channel,
                    opted_out=opted_out,
                    updated_at=updated_at,
                )
            )
        else:
            profile.name = name or profile.name
            profile.preferred_channel = preferred_channel or profile.preferred_channel
            profile.opted_out = opted_out or profile.opted_out
            profile.updated_at = updated_at
        session.commit()


def record_conversation(event: ConversationIngest) -> ConversationIngest:
    _upsert_profile(event.customer_id, event.customer_name, event.channel.value, event.opted_out, event.occurred_at)
    with SessionLocal() as session:
        session.add(
            IngestedConversationRecord(
                customer_id=event.customer_id,
                provider=event.provider.value,
                channel=event.channel.value,
                text=event.text,
                intent=event.intent.value,
                occurred_at=event.occurred_at,
            )
        )
        session.commit()
    return event


def record_order(event: StorefrontOrderIngest) -> StorefrontOrderIngest:
    _upsert_profile(event.customer_id, event.customer_name, "instagram_dm", False, datetime.combine(event.ordered_at, datetime.min.time()))
    with SessionLocal() as session:
        row = session.get(IngestedOrderRecord, event.order_id)
        if row is None:
            session.add(
                IngestedOrderRecord(
                    order_id=event.order_id,
                    customer_id=event.customer_id,
                    amount=event.amount,
                    used_discount_code=event.used_discount_code,
                    ordered_at=event.ordered_at,
                    provider=event.provider.value,
                )
            )
        else:
            row.amount = event.amount
            row.used_discount_code = event.used_discount_code
            row.ordered_at = event.ordered_at
            row.provider = event.provider.value
        session.commit()
    return event


def record_cart(event: StorefrontCartIngest) -> StorefrontCartIngest:
    _upsert_profile(event.customer_id, event.customer_name, "instagram_dm", False, event.updated_at)
    with SessionLocal() as session:
        row = session.get(IngestedCartRecord, event.customer_id)
        if row is None:
            session.add(
                IngestedCartRecord(
                    customer_id=event.customer_id,
                    status=event.status.value,
                    items_value=event.items_value,
                    abandon_stage=event.abandon_stage.value,
                    updated_at=event.updated_at,
                    distinct_categories=event.distinct_categories,
                    provider=event.provider.value,
                )
            )
        else:
            row.status = event.status.value
            row.items_value = event.items_value
            row.abandon_stage = event.abandon_stage.value
            row.updated_at = event.updated_at
            row.distinct_categories = event.distinct_categories
            row.provider = event.provider.value
        session.commit()
    return event


def get_customer_snapshot(customer_id: str) -> CustomerSnapshot | None:
    with SessionLocal() as session:
        profile = session.get(CustomerProfileRecord, customer_id)
        if profile is None:
            return None
        orders = (
            session.query(IngestedOrderRecord)
            .filter(IngestedOrderRecord.customer_id == customer_id)
            .order_by(IngestedOrderRecord.ordered_at)
            .all()
        )
        conversations = (
            session.query(IngestedConversationRecord)
            .filter(IngestedConversationRecord.customer_id == customer_id)
            .order_by(IngestedConversationRecord.occurred_at.desc())
            .limit(20)
            .all()
        )
        cart = session.get(IngestedCartRecord, customer_id)

    customer = Customer(
        customer_id=profile.customer_id,
        name=profile.name,
        preferred_channel=profile.preferred_channel,
        opted_out=profile.opted_out,
        orders=[
            Order(
                order_id=order.order_id,
                amount=order.amount,
                used_discount_code=order.used_discount_code,
                ordered_at=order.ordered_at,
            )
            for order in orders
        ],
        cart=CartEvent(
            status=cart.status,
            items_value=cart.items_value,
            abandon_stage=cart.abandon_stage,
            updated_at=_as_utc(cart.updated_at),
            distinct_categories=cart.distinct_categories,
        )
        if cart
        else CartEvent(),
        recent_conversations=[
            ConversationEvent(
                channel=conversation.channel,
                text=conversation.text,
                intent=conversation.intent,
                occurred_at=_as_utc(conversation.occurred_at),
            )
            for conversation in conversations
        ],
    )
    return CustomerSnapshot(customer=customer, order_count=len(orders), conversation_count=len(conversations))
