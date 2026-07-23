"""Action catalog metadata — matches docs/PRD.md section 5.4."""

from app.models import Action

ACTION_METADATA: dict[Action, dict] = {
    Action.REMINDER: {"label_fa": "یادآوری ساده", "cost_tier": "صفر", "urgency": "low"},
    Action.FREE_SHIPPING: {"label_fa": "ارسال رایگان", "cost_tier": "کم", "urgency": "medium"},
    Action.DISCOUNT_PERCENT: {"label_fa": "تخفیف هدفمند", "cost_tier": "متوسط", "urgency": "medium"},
    Action.CASHBACK: {"label_fa": "بازگشت وجه", "cost_tier": "متوسط", "urgency": "medium"},
    Action.BNPL_OFFER: {"label_fa": "خرید اقساطی/اعتباری", "cost_tier": "صفر (کارمزد پرداخت)", "urgency": "high"},
    Action.BUNDLE_OFFER: {"label_fa": "پیشنهاد بسته‌ای", "cost_tier": "کم", "urgency": "medium"},
    Action.VIP_NO_DISCOUNT: {"label_fa": "مشتری ویژه بدون تخفیف", "cost_tier": "صفر", "urgency": "low"},
    Action.WIN_BACK: {"label_fa": "بازگرداندن مشتری در ریسک ریزش", "cost_tier": "بالا", "urgency": "high"},
    Action.DO_NOT_DISTURB: {"label_fa": "عدم تماس", "cost_tier": "صفر", "urgency": "low"},
}
