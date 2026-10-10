import Link from "next/link";
import { PageShell } from "../../components/site-shell";

const plans = [
  ["شروع", "برای فروشگاه‌هایی که می‌خواهند تصمیم‌های نبض را روی یک بخش از مشتریان امتحان کنند.", ["راه‌اندازی اولیه", "صف تصمیم‌ها", "پشتیبانی ایمیلی"]],
  ["رشد", "برای تیم‌هایی که می‌خواهند تصمیم‌گیری را به جریان روزانهٔ فروش اضافه کنند.", ["همگام‌سازی داده", "گزارش کمپین", "بازبینی تصمیم‌ها"]],
  ["سازمانی", "برای فروشگاه‌های بزرگ‌تر با نیاز به اتصال و جریان اختصاصی.", ["اتصال اختصاصی", "کنترل‌های دسترسی", "پشتیبانی اولویت‌دار"]],
];

export default function PricingPage() {
  return <PageShell><section className="page-hero"><div className="container narrow"><p className="eyebrow">پلن‌ها</p><h1>با اندازهٔ فروشگاهتان شروع کنید.</h1><p>قیمت‌گذاری نهایی بر اساس حجم داده، کانال‌های متصل و نیازهای عملیاتی فروشگاه شما تعیین می‌شود.</p></div></section><section className="section"><div className="container plan-grid">{plans.map(([title, text, items], index) => <article className={`plan ${index === 1 ? "plan-featured" : ""}`} key={title as string}>{index === 1 && <span className="plan-badge">پیشنهاد نبض</span>}<h2>{title}</h2><p>{text}</p><ul>{(items as string[]).map((item) => <li key={item}>{item}</li>)}</ul><Link className={index === 1 ? "button" : "button button-ghost"} href="/request-demo">گفتگو دربارهٔ پلن</Link></article>)}</div></section><section className="section section-muted"><div className="container narrow centered"><p className="eyebrow">بدون ابهام</p><h2>اول ارزش محصول را ببینید.</h2><p>در جلسه دمو، وضعیت فروشگاه شما را می‌فهمیم و مسیر مناسب شروع را مشخص می‌کنیم.</p></div></section></PageShell>;
}
