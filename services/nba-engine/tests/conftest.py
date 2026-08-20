"""تنظیم محیط تست — پیش از import هر ماژول app، دیتابیس را به یک فایل SQLite
موقت وصل می‌کند تا تست‌ها روی nba_dev.db واقعی توسعه اثر نگذارند و هر اجرای
pytest با دیتابیس تازه شروع شود.
"""

import os
import tempfile

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mktemp(suffix='.db')}"
os.environ.setdefault("NBA_API_KEYS", "")

from app.db import init_db  # noqa: E402  (باید بعد از تنظیم DATABASE_URL باشد)

init_db()
