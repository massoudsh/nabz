# nba-engine — موتور تصمیم‌ساز نبض (Next-Best-Action)

سرویس API که با گرفتن داده‌ی یک مشتری (سفارش‌ها، سبد، مکالمات)، بهترین اقدام بعدی
(چه اقدام، چه کانال، چه پیام فارسی) را برمی‌گرداند. جزئیات منطق در `/project/docs/PRD.md`
و `/project/docs/ARCHITECTURE.md`.

## اجرا

```bash
cd services/nba-engine
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

مستندات تعاملی API: `http://127.0.0.1:8000/docs`

## تست

```bash
.venv/bin/python -m pytest tests/ -v
```

## نمونه درخواست

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

## بازخورد (Feedback Loop — آماده‌سازی فاز ۲)

نتیجه‌ی واقعی یک اقدام پیشنهادی (باز شد؟ خرید شد؟) با `POST /feedback` ثبت می‌شود
و با `GET /feedback/{customer_id}` قابل بازخوانی است. در MVP این داده فقط درون‌حافظه
ذخیره می‌شود (`app/feedback_store.py`)؛ در فاز ۱ جایش را جدول `CampaignHistory` در
Postgres می‌گیرد (`docs/ARCHITECTURE.md` بخش ۲ و ۶).

```bash
curl -X POST http://127.0.0.1:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"c_shipping","action":"free_shipping","channel":"whatsapp","opened":true,"purchased":true}'
```

## ساختار

```
app/
  models.py           # اسکیمای ورودی/خروجی (Pydantic) + CampaignFeedback
  engine.py           # استخراج سیگنال + قوانین تصمیم
  catalog.py          # کاتالوگ اقدام‌ها
  channels.py         # قالب پیام فارسی به تفکیک کانال
  feedback_store.py   # ذخیره‌ی درون‌حافظه‌ای بازخورد (MVP)
  main.py             # FastAPI app — /health, /decide, /feedback
examples/sample_customers.json  # ۶ پرسونای نمونه مطابق PRD
tests/test_engine.py            # تست رفتار موتور برای هر پرسونا (تاریخ‌ها نسبت به امروز جابه‌جا می‌شوند)
tests/test_feedback.py          # تست ثبت/بازخوانی بازخورد
```
