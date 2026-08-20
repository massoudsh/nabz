"""احراز هویت ساده با API key — issue #7 / docs/ARCHITECTURE.md بخش ۷.

کلید از متغیر محیطی ``NBA_API_KEYS`` خوانده می‌شود (یک یا چند کلید جدا‌شده
با کاما، برای امکان چرخش کلید بدون قطعی). اگر این متغیر تنظیم نشده باشد
(مثلاً محیط توسعه‌ی محلی)، سرویس بدون احراز هویت اجرا می‌شود تا کار توسعه
مسدود نشود — ولی هر استقرار واقعی باید آن را تنظیم کند.

کلید هم به‌صورت هدر ``X-API-Key`` (برای فراخوانی API) و هم به‌صورت پارامتر
Query به نام ``api_key`` (برای صفحه‌ی /admin در مرورگر) پذیرفته می‌شود.
"""

from __future__ import annotations

import os

from fastapi import Header, HTTPException, Query, status


def _configured_keys() -> set[str]:
    raw = os.environ.get("NBA_API_KEYS", "")
    return {k.strip() for k in raw.split(",") if k.strip()}


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    api_key: str | None = Query(default=None),
) -> None:
    keys = _configured_keys()
    if not keys:
        # هیچ کلیدی تنظیم نشده → محیط توسعه، بدون احراز هویت
        return
    provided = x_api_key or api_key
    if provided not in keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key نامعتبر یا ارسال‌نشده (هدر X-API-Key)",
        )
