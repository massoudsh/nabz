# معماری و مدل داده — نبض (Nabz)

## ۱. نمای کلی سیستم

```
                     ┌─────────────────────────┐
   منابع داده  ───▶  │   Ingestion Layer        │   (فاز ۱: اتصال واقعی به
 (فروشگاه‌ساز،        │   (این نسخه: JSON ورودی) │    اینستاگرام/واتساپ بیزینس/
  اینستاگرام،                                    │    فروشگاه‌ساز)
  واتساپ بیزینس)      └────────────┬─────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────┐
                     │   Signal Extraction      │  RFM, حساسیت به تخفیف/ارسال,
                     │                          │  ریسک ریزش, نیت مکالمه
                     └────────────┬─────────────┘
                                   ▼
                     ┌─────────────────────────┐
                     │   Decision Engine (NBA)  │  کاتالوگ اقدام + قوانین اولویت
                     │   services/nba-engine    │  + امتیازدهی
                     └────────────┬─────────────┘
                                   ▼
                     ┌─────────────────────────┐
                     │   Channel & Message Gen  │  انتخاب کانال + قالب پیام فارسی
                     └────────────┬─────────────┘
                                   ▼
                     ┌─────────────────────────┐
                     │   Decision Output (API)  │  → مصرف توسط پنل/فروشنده/
                     │                          │    ابزار ارسال (فاز ۳)
                     └────────────┬─────────────┘
                                   ▼
                     ┌─────────────────────────┐
                     │   Feedback Store          │  نتیجه‌ی هر اقدام (فاز ۲)
                     └─────────────────────────┘
```

در فاز MVP فقط سه بخش میانی (Signal Extraction → Decision Engine → Channel & Message Gen)
به‌صورت یک سرویس API واحد (`services/nba-engine`) پیاده‌سازی شده‌اند؛ ورودی/خروجی به شکل JSON است
تا اتصال به هر منبع داده‌ی واقعی در فاز ۱ ساده باشد.

## ۲. مدل داده (Schema)

### Customer
| فیلد | نوع | توضیح |
|---|---|---|
| customer_id | string | شناسه یکتا |
| name | string | نام (برای شخصی‌سازی پیام) |
| preferred_channel | enum(instagram_dm, whatsapp, sms) | کانال ترجیحی |
| opted_out | bool | مشتری درخواست عدم تماس داده |
| max_messages_per_week | int | سقف فرکانس پیام |
| messages_sent_last_7_days | int | تعداد پیام ارسالی هفته اخیر |
| joined_at | date | تاریخ عضویت |

### Order (تاریخچه سفارش)
| فیلد | نوع | توضیح |
|---|---|---|
| order_id | string | |
| customer_id | string | |
| amount | number | مبلغ (تومان) |
| used_discount_code | bool | آیا با کد تخفیف خرید کرده |
| ordered_at | date | |

### CartEvent (سبد فعلی/رهاشده)
| فیلد | نوع | توضیح |
|---|---|---|
| customer_id | string | |
| items_value | number | ارزش سبد |
| status | enum(abandoned, active, completed) | |
| abandon_stage | enum(shipping_cost_seen, payment_page, none) | مرحله‌ی رهاشدن |
| updated_at | datetime | |

### ConversationEvent (دایرکت/واتساپ)
| فیلد | نوع | توضیح |
|---|---|---|
| customer_id | string | |
| channel | enum(instagram_dm, whatsapp) | |
| text | string | متن پیام مشتری (برای استخراج نیت) |
| intent | enum(price_question, complaint, interest, none) | برچسب نیت (قابل استخراج با NLP در فاز بعد) |
| occurred_at | datetime | |

### StoryReaction
| فیلد | نوع | توضیح |
|---|---|---|
| customer_id | string | |
| reacted_at | datetime | |

### CampaignHistory (بازخورد فاز ۲)
| فیلد | نوع | توضیح |
|---|---|---|
| customer_id | string | |
| action | string | اقدامی که پیشنهاد شد |
| channel | string | |
| opened | bool | |
| purchased | bool | |
| sent_at | datetime | |

## ۳. پایپلاین سیگنال‌سازی (Signal Extraction)

هر سیگنال یک تابع محض (pure function) روی داده‌ی مشتری است و عددی بین ۰ تا ۱ برمی‌گرداند:

- **recency_score** — هرچه از آخرین خرید بیشتر گذشته باشد نسبت به میانگین بازه‌ی تکرار خرید همان مشتری، نزدیک‌تر به ۱ (ریسک ریزش بالاتر).
- **frequency_score** — نرمال‌شده بر اساس تعداد سفارش‌ها.
- **discount_sensitivity** — نسبت سفارش‌های با کد تخفیف به کل سفارش‌ها.
- **shipping_sensitivity** — نسبت دفعات رهاشدن سبد در مرحله‌ی `shipping_cost_seen` به کل رهاشدن‌ها.
- **cart_urgency** — بر اساس تازگی و ارزش سبد رهاشده.
- **churn_risk** — ترکیب recency_score و بازه‌ی معمول خرید مشتری (اگر مدت‌زمان از آخرین خرید > ۱.۵ برابر میانگین بازه‌ی خرید مشتری → ریسک بالا).
- **conversation_intent_signal** — اگر آخرین پیام مکالمه intent=price_question یا interest داشته و بدون پاسخ‌گویی به خرید مانده.
- **contact_budget_remaining** — `max_messages_per_week - messages_sent_last_7_days`؛ اگر ≤ ۰ → مسیر مستقیم به `do_not_disturb`.

این امتیازها در `services/nba-engine/app/engine.py` پیاده‌سازی شده‌اند.

## ۴. منطق انتخاب اقدام (Decision Rules)

قوانین به ترتیب اولویت اجرا می‌شوند (اولین قانونی که match شود، تعیین‌کننده است):

1. `opted_out == true` یا `contact_budget_remaining <= 0` → `do_not_disturb`
2. `churn_risk >= 0.7` → `win_back` (پیام فوری، کانال با بالاترین نرخ پاسخ مشتری)
3. `cart status == abandoned` و `abandon_stage == payment_page` و `items_value` بالاتر از میانگین سبد فروشگاه → `bnpl_offer`
4. `cart status == abandoned` و `abandon_stage == shipping_cost_seen` و `shipping_sensitivity >= 0.5` → `free_shipping`
5. `discount_sensitivity <= 0.15` و `frequency_score >= 0.5` → `vip_no_discount` (بدون تخفیف؛ صرفاً یادآوری محصول جدید)
6. `conversation_intent_signal == price_question` و بدون خرید در ۴۸ ساعت اخیر → `discount_percent` (تخفیف هدفمند کوتاه‌مدت)
7. `frequency_score >= 0.6` و `discount_sensitivity` متوسط → `cashback` (به‌جای تخفیف آنی)
8. سبد شامل چند دسته‌ی مرتبط بدون رهاشدن → `bundle_offer`
9. پیش‌فرض (هیچ‌کدام match نشد) → `reminder`

هر قانون در خروجی، دلیل (`reasoning`) قابل‌خواندن برای انسان تولید می‌کند تا فروشنده به تصمیم اعتماد کند
(شفافیت به‌جای جعبه سیاه).

## ۵. چرا قانون‌محور در MVP، نه ML؟

برای اعتبارسنجی اولیه با خرده‌فروش‌های واقعی، داده‌ی تاریخی کافی برای آموزش مدل وجود ندارد.
موتور قانون‌محور + امتیازدهی، قابل توضیح است (فروشنده می‌فهمد چرا این تصمیم گرفته شده)
و ساختار `CampaignHistory` از روز اول برای فاز ۲ (یادگیری از بازخورد واقعی) آماده شده است.

## ۶. پشته‌ی فنی MVP

- **زبان/فریم‌ورک:** Python 3.12 + FastAPI (سبک، مستندسازی خودکار OpenAPI، مناسب سرویس تصمیم‌ساز).
- **اعتبارسنجی داده:** Pydantic.
- **تست:** pytest.
- **دیتابیس:** SQLAlchemy با `DATABASE_URL` قابل‌تنظیم — Postgres در production، SQLite برای توسعه/تست محلی (بدون نیاز به سرور دیتابیس). جدول‌های `campaign_history` (CampaignHistory) و `decisions` (لاگ پنل مدیریتی) در startup ساخته می‌شوند.
- **استقرار:** طبق راهنمای بیلد پروژه، بیلد نهایی روی سرور SSH انجام می‌شود، نه داخل کانتینر توسعه — جزئیات کامل در `docs/DEPLOYMENT.md`.

## ۷. نکات امنیتی و حریم خصوصی

- داده‌ی مکالمه (متن دایرکت/واتساپ) حاوی اطلاعات شخصی است؛ در فاز ۱ باید رمزنگاری در حالت سکون (at rest) و کنترل دسترسی داشته باشد.
- فیلد `opted_out` باید در بالاترین اولویت قانون‌ها بررسی شود (که همین‌طور است) تا رعایت رضایت مشتری تضمین شود.
- در فاز اتصال به API رسمی واتساپ بیزینس/اینستاگرام، فقط از APIهای رسمی و مجاز پلتفرم استفاده شود؛ scraping یا دور زدن محدودیت پلتفرم‌ها در scope این پروژه نیست.
- **احراز هویت:** همه‌ی endpointهای API (بجز `/health`) با API key (`NBA_API_KEY`s، هدر `X-API-Key`) قابل محافظت‌اند — `app/auth.py`. تنظیم آن پیش از استقرار عمومی الزامی است.
