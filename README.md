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
  web/              # فرانت‌اند عمومی Next.js برای مشتریان و ذی‌نفعان
```

## شروع سریع با Docker

پیش‌نیاز: Docker و Docker Compose نصب‌شده روی سیستم.

```bash
# از ریشهٔ پروژه
docker compose up --build
```

سرویس‌ها:

- فرانت‌اند: http://localhost:3000
- API و مستندات: http://localhost:8000/docs
- سلامت API: http://localhost:8000/health
- پنل مدیریتی: http://localhost:8000/admin

اجرای پس‌زمینه، مشاهده لاگ و توقف:

```bash
docker compose up --build -d
docker compose logs -f
docker compose down
```

دادهٔ PostgreSQL در volume به نام `postgres_data` باقی می‌ماند. برای حذف دادهٔ دیتابیس نیز:

```bash
docker compose down -v
```

برای فعال‌کردن API key، پیش از اجرا متغیرهای محیطی را تنظیم کنید:

```bash
export POSTGRES_PASSWORD="یک-رمز-قوی"
export NBA_API_KEYS="dev-key-1"
docker compose up --build
```

### استفاده از registry mirror یا image محلی

اگر شبکه‌ی Docker به Docker Hub دسترسی ندارد، imageهای پایه را با متغیرهای محیطی جایگزین کنید:

```bash
export POSTGRES_IMAGE="registry.example.com/postgres:16-alpine"
export PYTHON_IMAGE="registry.example.com/python:3.12-slim"
export NODE_IMAGE="registry.example.com/node:22-alpine"
docker compose up -d --build
```

اگر imageها از قبل روی سیستم موجودند، از pull دوباره جلوگیری کنید:

```bash
docker compose up -d --build --pull never
```

### خطای `Get "https://registry-1.docker.io/v2/": EOF`

این خطا مربوط به دسترسی daemon داکر به registry است، نه به کد پروژه. `curl https://registry-1.docker.io/v2/` که پاسخ `401` می‌دهد طبیعی است (endpoint بدون توکن همیشه 401 برمی‌گرداند) و فقط نشان می‌دهد شبکهٔ shell سالم است.

1. تکرار pull — خطای `EOF` معمولاً موقتی است:

   ```bash
   docker pull postgres:16-alpine
   ```

2. تنظیم پروکسی برای daemon (اگر پروکسی دارید) در `~/.docker/config.json`:

   ```json
   {
     "proxies": {
       "default": {
         "httpProxy": "http://PROXY_HOST:PROXY_PORT",
         "httpsProxy": "http://PROXY_HOST:PROXY_PORT",
         "noProxy": "localhost,127.0.0.1"
       }
     }
   }
   ```

   سپس `sudo systemctl restart docker`.

3. تنظیم DNS یا mirror در `/etc/docker/daemon.json`:

   ```json
   {
     "dns": ["8.8.8.8", "1.1.1.1"],
     "registry-mirrors": ["https://YOUR_MIRROR"]
   }
   ```

   سپس `sudo systemctl restart docker`.

4. صحت تنظیمات daemon را بررسی کنید:

   ```bash
   docker info | grep -iE 'proxy|registry|mirror'
   ```

## اجرای محلی بدون Docker

```bash
# موتور تصمیم‌ساز
cd services/nba-engine
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload

# در ترمینال دوم، فرانت‌اند عمومی
cd apps/web
npm install
npm run dev
```

## اسناد

- [PRD کامل محصول](docs/PRD.md)
- [معماری و مدل داده](docs/ARCHITECTURE.md)
- [README سرویس nba-engine](services/nba-engine/README.md)
