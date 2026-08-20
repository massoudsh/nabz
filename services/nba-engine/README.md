# nba-engine — موتور تصمیم‌ساز نبض (Next-Best-Action)

سرویس API که با گرفتن داده‌ی یک مشتری (سفارش‌ها، سبد، مکالمات)، بهترین اقدام بعدی
(چه اقدام، چه کانال، چه پیام فارسی) را برمی‌گرداند. جزئیات منطق در `/project/docs/PRD.md`
و `/project/docs/ARCHITECTURE.md`. راهنمای استقرار production: `/project/docs/DEPLOYMENT.md`.

## اجرا

```bash
cd services/nba-engine
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

مستندات تعاملی API: `http://127.0.0.1:8000/docs`
پنل مدیریتی (لیست تصمیم‌ها + تایید/رد): `http://127.0.0.1:8000/admin`

## احراز هویت (API key)

اگر متغیر محیطی `NBA_API_KEYS` تنظیم شده باشد (یک یا چند کلید جدا‌شده با کاما)،
تمام endpointها بجز `/health` به هدر `X-API-Key` نیاز دارند (یا پارامتر Query به
نام `api_key` برای صفحه‌ی مرورگرمحور `/admin`). اگر تنظیم نشود (پیش‌فرض توسعه‌ی
محلی)، سرویس بدون احراز هویت اجرا می‌شود — برای production حتماً تنظیم شود.

```bash
export NBA_API_KEYS="dev-key-1"
curl -X POST http://127.0.0.1:8000/decide -H "X-API-Key: dev-key-1" -d '...'
```

## دیتابیس

آدرس از `DATABASE_URL` خوانده می‌شود (پیش‌فرض SQLite محلی برای توسعه:
`sqlite:///./nba_dev.db`؛ در production باید به Postgres اشاره کند، مثلاً
`postgresql+psycopg2://user:pass@host:5432/nabz`). جدول‌ها (`campaign_history`,
`decisions`) در startup اپ خودکار ساخته می‌شوند.

## تست

```bash
.venv/bin/python -m pytest tests/ -v
```

تست‌ها از یک فایل SQLite موقت جدا از `nba_dev.db` استفاده می‌کنند (`tests/conftest.py`).

## endpointها

| Method/Path | توضیح |
|---|---|
| `GET /health` | بدون نیاز به API key |
| `POST /decide` | تصمیم برای یک مشتری؛ در `decisions` هم لاگ می‌شود |
| `POST /decide/batch` | تصمیم برای لیستی از مشتری‌ها یکجا |
| `POST /feedback` | ثبت نتیجه‌ی واقعی یک اقدام (باز شد/خرید شد) |
| `GET /feedback/{customer_id}` | بازخوانی تاریخچه‌ی بازخورد یک مشتری |
| `GET /admin` | داشبورد HTML — لیست تصمیم‌ها + فیلتر وضعیت |
| `POST /admin/decisions/{id}/approve` | تایید یک تصمیم |
| `POST /admin/decisions/{id}/reject` | رد یک تصمیم |

### نمونه درخواست تک‌مشتری

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d @examples/sample_customers.json   # (یک پرسونا را جدا انتخاب کنید، فایل شامل چند نمونه است)
```

پاسخ نمونه:

```json
{
  "customer_id": "c_shipping",
  "recommended_action": "free_shipping",
  "channel": "whatsapp",
  "urgency": "medium",
  "message_fa": "سلام مریم جان، سبدت هنوز منتظرته! امروز ارسال رایگانه، دوست داری تکمیلش کنیم؟",
  "reasoning": ["سبد هنگام دیدن هزینه ارسال رها شده و حساسیت به ارسال بالاست (1.0)"],
  "confidence": 0.9,
  "do_not_disturb": false,
  "signals": { "...": "..." }
}
```

### نمونه درخواست دسته‌ای

```bash
curl -X POST http://127.0.0.1:8000/decide/batch \
  -H "Content-Type: application/json" \
  -d '[{"customer_id":"c1"}, {"customer_id":"c2"}]'
```

## بازخورد و امتیازدهی تطبیقی (فاز ۲)

نتیجه‌ی واقعی یک اقدام پیشنهادی (باز شد؟ خرید شد؟) با `POST /feedback` ثبت می‌شود
و در جدول `campaign_history` (Postgres/SQLite) پایدار می‌ماند. موتور تصمیم
(`app/engine.py`) از نرخ خرید واقعی هر اقدام (در صورت وجود حداقل ۳ نمونه) برای
تنظیم `confidence` تا سقف `±۰.۱۵` استفاده می‌کند — به‌جای وزن ثابت قبلی.

```bash
curl -X POST http://127.0.0.1:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"c_shipping","action":"free_shipping","channel":"whatsapp","opened":true,"purchased":true}'
```

## ساختار

```
app/
  models.py           # اسکیمای ورودی/خروجی (Pydantic) + CampaignFeedback
  engine.py           # استخراج سیگنال + قوانین تصمیم + امتیازدهی تطبیقی
  catalog.py          # کاتالوگ اقدام‌ها
  channels.py         # قالب پیام فارسی به تفکیک کانال
  db.py                # اتصال SQLAlchemy (Postgres/SQLite بر اساس DATABASE_URL)
  feedback_store.py   # جدول CampaignHistory (پایدار)
  decision_store.py   # لاگ تصمیم‌ها برای پنل مدیریتی (approve/reject)
  auth.py             # احراز هویت API key
  admin.py             # روتر پنل مدیریتی (/admin)
  templates/admin.html # قالب Jinja2 داشبورد
  main.py             # FastAPI app — همه‌ی endpointها
examples/sample_customers.json  # ۶ پرسونای نمونه مطابق PRD
tests/                          # ۲۲ تست (موتور، بازخورد، دسته‌ای، احراز هویت، پنل، امتیازدهی تطبیقی)
```
