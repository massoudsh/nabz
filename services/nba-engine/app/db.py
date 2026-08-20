"""لایه‌ی اتصال دیتابیس — docs/ARCHITECTURE.md بخش ۶ (فاز ۱: اتصال به Postgres).

آدرس اتصال از متغیر محیطی ``DATABASE_URL`` خوانده می‌شود (مثلاً
``postgresql+psycopg2://user:pass@host:5432/nabz``). اگر تنظیم نشده باشد،
برای توسعه‌ی محلی و تست به یک فایل SQLite کنار سرویس سقوط می‌کند — بدون نیاز
به سرور دیتابیس واقعی برای اجرای تست‌ها. در استقرار واقعی (سرور SSH طبق
قانون بیلد پروژه)، ``DATABASE_URL`` باید به یک نمونه‌ی Postgres اشاره کند.
"""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./nba_dev.db")

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    """ساخت جدول‌ها در صورت نبود — روی FastAPI startup صدا زده می‌شود."""
    from app import decision_store, feedback_store  # noqa: F401  (ثبت مدل‌ها روی Base)

    Base.metadata.create_all(bind=engine)
