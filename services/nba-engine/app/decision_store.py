"""لاگ تصمیم‌های صادرشده — پایه‌ی پنل مدیریتی فروشنده (issue #3).

هر بار /decide یا /decide/batch صدا زده می‌شود، تصمیم با وضعیت ``pending``
ثبت می‌شود. فروشنده از طریق /admin می‌تواند آن را approve/reject کند —
گام اول «رابط گرافیکی برای دیدن لیست تصمیم‌ها، تایید/رد پیشنهاد» طبق
docs/PRD.md بخش ۷/۸.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base, SessionLocal
from app.models import Decision

VALID_STATUSES = ("pending", "approved", "rejected")


class DecisionRecord(Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(String, index=True)
    action: Mapped[str] = mapped_column(String)
    channel: Mapped[str] = mapped_column(String)
    message_fa: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float)
    urgency: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


@dataclass
class DecisionLogEntry:
    id: str
    customer_id: str
    action: str
    channel: str
    message_fa: str
    confidence: float
    urgency: str
    status: str
    created_at: datetime


def log_decision(decision: Decision) -> str:
    decision_id = str(uuid.uuid4())
    with SessionLocal() as session:
        session.add(
            DecisionRecord(
                id=decision_id,
                customer_id=decision.customer_id,
                action=decision.recommended_action.value,
                channel=decision.channel.value,
                message_fa=decision.message_fa,
                confidence=decision.confidence,
                urgency=decision.urgency,
                status="pending",
                created_at=datetime.now(timezone.utc),
            )
        )
        session.commit()
    return decision_id


def list_decisions(status: str | None = None, limit: int = 200) -> list[DecisionLogEntry]:
    with SessionLocal() as session:
        query = session.query(DecisionRecord)
        if status:
            query = query.filter(DecisionRecord.status == status)
        rows = query.order_by(DecisionRecord.created_at.desc()).limit(limit).all()
        return [
            DecisionLogEntry(
                id=r.id,
                customer_id=r.customer_id,
                action=r.action,
                channel=r.channel,
                message_fa=r.message_fa,
                confidence=r.confidence,
                urgency=r.urgency,
                status=r.status,
                created_at=r.created_at,
            )
            for r in rows
        ]


def set_status(decision_id: str, status: str) -> bool:
    if status not in VALID_STATUSES:
        raise ValueError(f"وضعیت نامعتبر: {status}")
    with SessionLocal() as session:
        row = session.get(DecisionRecord, decision_id)
        if row is None:
            return False
        row.status = status
        session.commit()
        return True
