# استقرار (Deployment) — نبض

طبق قانون بیلد پروژه (`docs/ARCHITECTURE.md` بخش ۶): **هیچ بیلد سنگینی داخل کانتینر
توسعه اجرا نمی‌شود.** تست‌های سبک (pytest) در همین کانتینر و در CI اجرا می‌شوند؛
نصب production، اجرای سرویس، و هر عملیات سنگین‌تر باید روی سرور SSH انجام شود.

## ۱. یکپارچه‌سازی مداوم (CI)

`.github/workflows/ci.yml` روی هر push/PR به `master`، وابستگی‌های `services/nba-engine`
را نصب و `pytest` را اجرا می‌کند (روی runner گیت‌هاب، نه کانتینر توسعه — پس محدودیت
بیلد سنگین اینجا اثر ندارد؛ کار سبک است: نصب pip + اجرای تست).

## ۲. استقرار nba-engine (روی سرور SSH)

### پیش‌نیاز
- Python 3.12
- یک نمونه‌ی Postgres در دسترس (`DATABASE_URL`) — طبق `docs/ARCHITECTURE.md` بخش ۶.

### مراحل (روی سرور، نه کانتینر توسعه)

```bash
cd /path/on/server
git clone <repo-url> nabz && cd nabz/services/nba-engine
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# متغیرهای محیطی production
export DATABASE_URL="postgresql+psycopg2://nabz_user:PASSWORD@localhost:5432/nabz"
export NBA_API_KEYS="کلید-تولید-۱,کلید-تولید-۲"   # الزامی؛ خالی بودن یعنی بدون احراز هویت

.venv/bin/gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --workers 2
```

جدول‌های Postgres (`campaign_history`, `decisions`) در startup اپ به‌صورت خودکار
ساخته می‌شوند (`app/db.py::init_db`) — نیازی به migration دستی در MVP نیست.

### systemd service (نمونه)

```ini
# /etc/systemd/system/nba-engine.service
[Unit]
Description=Nabz NBA Engine
After=network.target postgresql.service

[Service]
WorkingDirectory=/path/on/server/nabz/services/nba-engine
Environment=DATABASE_URL=postgresql+psycopg2://nabz_user:PASSWORD@localhost:5432/nabz
Environment=NBA_API_KEYS=کلید-تولید-۱
ExecStart=/path/on/server/nabz/services/nba-engine/.venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

سپس یک reverse proxy (nginx/caddy) روی دامنه‌ی مربوطه به `127.0.0.1:8000` وصل شود
(با TLS). `X-API-Key` باید توسط مصرف‌کننده‌های API ارسال شود؛ `/admin` هم با همان
کلید از طریق پارامتر `?api_key=` در مرورگر قابل دسترسی است.

## ۳. استقرار لندینگ (`apps/landing`)

فایل استاتیک (`index.html`) نیاز به بیلد ندارد — مستقیم روی هر static hosting
(nginx، Cloudflare Pages، یا کنار همان سرور nba-engine با nginx) قابل serve است.

```bash
# نمونه با nginx: کپی فایل به webroot دامنه‌ی لندینگ
cp apps/landing/index.html /var/www/nabz-landing/index.html
```

## ۴. چک‌لیست پیش از استقرار عمومی

- [ ] `NBA_API_KEYS` تنظیم شده (خالی نگذارید — issue #7).
- [ ] `DATABASE_URL` به Postgres واقعی اشاره می‌کند، نه SQLite توسعه.
- [ ] TLS روی reverse proxy فعال است (داده‌ی مکالمه مشتری حساس است — `docs/ARCHITECTURE.md` بخش ۷).
- [ ] پشتیبان‌گیری دوره‌ای از Postgres (`campaign_history`, `decisions`) تنظیم شده.
