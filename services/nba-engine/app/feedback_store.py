"""ذخیره‌ی پایدار بازخورد کمپین — جدول ``CampaignHistory`` در Postgres/SQLite.

جایگزین نسخه‌ی درون‌حافظه‌ای MVP (docs/ARCHITECTURE.md بخش ۲ و ۶، فاز ۱).
رابط تابعی همان قبلی نگه داشته شده (``record`` / ``list_for_customer``) تا
app/main.py بدون تغییر بماند؛ علاوه بر آن ``purchase_rate_for_action`` برای
امتیازدهی تطبیقی فاز ۲ (``app/engine.py``) اضافه شده.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base, SessionLocal
from app.models import Action, CampaignFeedback, Channel


class CampaignHistoryRecord(Base):
    __tablename__ = "campaign_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(String, index=True)
    action: Mapped[str] = mapped_column(String)
    channel: Mapped[str] = mapped_column(String)
    opened: Mapped[bool] = mapped_column(Boolean, default=False)
    purchased: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_feedback(self) -> CampaignFeedback:
        return CampaignFeedback(
            customer_id=self.customer_id,
            action=Action(self.action),
            channel=Channel(self.channel),
            opened=self.opened,
            purchased=self.purchased,
            sent_at=self.sent_at,
        )


def record(feedback: CampaignFeedback) -> CampaignFeedback:
    with SessionLocal() as session:
        row = CampaignHistoryRecord(
            customer_id=feedback.customer_id,
            action=feedback.action.value,
            channel=feedback.channel.value,
            opened=feedback.opened,
            purchased=feedback.purchased,
            sent_at=feedback.sent_at,
        )
        session.add(row)
        session.commit()
    return feedback


def list_for_customer(customer_id: str) -> list[CampaignFeedback]:
    with SessionLocal() as session:
        rows = (
            session.query(CampaignHistoryRecord)
            .filter(CampaignHistoryRecord.customer_id == customer_id)
            .order_by(CampaignHistoryRecord.sent_at)
            .all()
        )
        return [row.to_feedback() for row in rows]


def purchase_rate_for_action(action: Action, min_samples: int = 3) -> float | None:
    """نرخ خرید واقعی (purchased=true) برای یک اقدام، در صورت داشتن نمونه‌ی کافی.

    برای امتیازدهی تطبیقی فاز ۲ در app/engine.py استفاده می‌شود؛ اگر نمونه کافی
    نباشد ``None`` برمی‌گرداند تا موتور به مقدار پیش‌فرض ثابت برگردد.
    """
    with SessionLocal() as session:
        rows = (
            session.query(CampaignHistoryRecord)
            .filter(CampaignHistoryRecord.action == action.value)
            .all()
        )
    if len(rows) < min_samples:
        return None
    return sum(1 for r in rows if r.purchased) / len(rows)
