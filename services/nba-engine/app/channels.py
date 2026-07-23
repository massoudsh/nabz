"""Persian message templates per (action, channel) — docs/PRD.md section 5.5."""

from app.models import Action, Channel

# قالب‌های پایه به‌ازای هر اقدام (placeholder: {name})
_BASE_TEMPLATES: dict[Action, str] = {
    Action.REMINDER: "سلام {name} جان، دلمون برات تنگ شده! محصولات جدید رو دیدی؟",
    Action.FREE_SHIPPING: "سلام {name} جان، سبدت هنوز منتظرته! امروز ارسال رایگانه، دوست داری تکمیلش کنیم؟",
    Action.DISCOUNT_PERCENT: "سلام {name} جان، برای همین محصولی که پرسیده بودی یه کد تخفیف ویژه داریم، می‌خوای برات بفرستم؟",
    Action.CASHBACK: "سلام {name} جان، این بار خریدت رو با کش‌بک جبران می‌کنیم! جزئیات رو برات بفرستم؟",
    Action.BNPL_OFFER: "سلام {name} جان، اگه بخوای می‌تونی این خرید رو قسطی/اعتباری تکمیل کنی، نیاز به پرداخت یکجا نیست.",
    Action.BUNDLE_OFFER: "سلام {name} جان، این محصول با چند تا از موارد سبدت ست میشه، دوست داری با هم پیشنهادش کنم؟",
    Action.VIP_NO_DISCOUNT: "سلام {name} جان، محصول جدیدمون اومده و فکر کردیم حتماً باید اول به تو نشونش بدیم 🙌",
    Action.WIN_BACK: "سلام {name} جان، خیلی وقته ندیدیمت! یه پیشنهاد ویژه فقط برای بازگشتت داریم.",
    Action.DO_NOT_DISTURB: "",
}

# تنظیمات لحن بر اساس کانال
_CHANNEL_STYLE = {
    Channel.INSTAGRAM_DM: {"emoji": True, "prefix": ""},
    Channel.WHATSAPP: {"emoji": True, "prefix": ""},
    Channel.SMS: {"emoji": False, "prefix": "فروشگاه شما: "},
}


def render_message(action: Action, channel: Channel, name: str) -> str:
    if action == Action.DO_NOT_DISTURB:
        return ""

    template = _BASE_TEMPLATES[action]
    text = template.format(name=name)

    style = _CHANNEL_STYLE[channel]
    if not style["emoji"]:
        # حذف ایموجی‌های رایج برای پیامک (کوتاه و رسمی‌تر)
        for emoji in ["🌸", "🙌", "😊", "✨"]:
            text = text.replace(emoji, "").strip()
    return f"{style['prefix']}{text}"
