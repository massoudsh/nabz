"""ذخیره‌ی درون‌حافظه‌ای بازخورد کمپین — MVP بدون دیتابیس (docs/ARCHITECTURE.md بخش ۶).

در فاز ۱ جای این ماژول را جدول Postgres (`CampaignHistory`) می‌گیرد؛ رابط تابعی
همینجا نگه داشته شده تا آن جایگزینی بدون تغییر در app/main.py ممکن باشد.
"""

from __future__ import annotations

from app.models import CampaignFeedback

_feedback: list[CampaignFeedback] = []


def record(feedback: CampaignFeedback) -> CampaignFeedback:
    _feedback.append(feedback)
    return feedback


def list_for_customer(customer_id: str) -> list[CampaignFeedback]:
    return [f for f in _feedback if f.customer_id == customer_id]
