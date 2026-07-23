# نبض (Nabz)

ایجنت تصمیم‌ساز نگه‌داشت مشتری برای خرده‌فروش‌های ایرانی.
برای هر مشتری، از دل داده‌ی خرید/سبد/مکالمه، **بهترین اقدام بعدی** را مشخص می‌کند:
چه کسی، چه زمانی، از چه کانالی، با چه پیشنهادی.

## ساختار پروژه

```
docs/
  PRD.md            # تعریف محصول: مسئله، پرسوناها، منطق تصمیم، کاتالوگ اقدام
  ARCHITECTURE.md   # معماری سیستم، مدل داده، پایپلاین سیگنال‌سازی

services/
  nba-engine/        # سرویس API موتور Next-Best-Action (Python/FastAPI، MVP)

apps/
  landing/            # لندینگ استاتیک برای اعتبارسنجی ایده
```

## شروع سریع

```bash
# موتور تصمیم‌ساز
cd services/nba-engine
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
# → http://127.0.0.1:8000/docs

# لندینگ
cd apps/landing
python3 -m http.server 8000
```

## اسناد

- [PRD کامل محصول](docs/PRD.md)
- [معماری و مدل داده](docs/ARCHITECTURE.md)
- [README سرویس nba-engine](services/nba-engine/README.md)
