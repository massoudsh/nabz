import Link from "next/link";
import { PageShell } from "../../components/site-shell";

const productFeatures = [
  ["اقدام مناسب", "از میان ۹ اقدام عملی، مناسب‌ترین گزینه را برای هر مشتری انتخاب می‌کند."],
  ["کانال مناسب", "دایرکت، واتساپ یا پیامک را با توجه به ترجیح مشتری پیشنهاد می‌دهد."],
  ["پیام آماده", "متن فارسی متناسب با کانال و زمینهٔ خرید مشتری آماده می‌شود."],
  ["دلیل روشن", "هر تصمیم همراه با سیگنال‌ها و استدلال قابل‌بررسی ارائه می‌شود."],
];

const competitiveFeatures = [
  ["نمای ۳۶۰ درجه مشتری", "سفارش، سبد، مکالمه، تصمیم و نتیجهٔ هر اقدام در یک خط زمانی قابل‌فهم کنار هم قرار می‌گیرند."],
  ["بخش‌بندی RFM و ارزش مشتری", "مشتری‌ها بر اساس تازگی، تکرار و ارزش خرید برای تصمیم‌های دقیق‌تر اولویت‌بندی می‌شوند."],
  ["زمان ارسال پیشنهادی", "به‌جای ارسال هم‌زمان، زمان مناسب ارتباط با توجه به رفتار هر مشتری پیشنهاد می‌شود."],
  ["محافظ سودآوری", "هزینهٔ تخفیف، کش‌بک و ارسال قبل از اجرا با حاشیه سود مقایسه می‌شود؛ کمپین زیان‌ده متوقف می‌ماند."],
  ["انتساب و یادگیری", "خریدهای بعد از هر اقدام به تصمیم مربوط می‌شوند تا اعتماد به پیشنهادها با دادهٔ واقعی بهتر شود."],
];

export default function ProductPage() {
  return <PageShell>
    <section className="page-hero"><div className="container narrow"><p className="eyebrow">محصول</p><h1>نبض، مغز تصمیم فروشگاه شماست.</h1><p>نبض روی ابزارهای فعلی شما می‌نشیند و به‌جای ارسال کمپین یکسان، مشخص می‌کند با کدام مشتری چه کاری انجام دهید.</p></div></section>
    <section className="section"><div className="container"><div className="card-grid two-columns">{productFeatures.map(([title, text], index) => <article className="feature-card" key={title}><span>۰{index + 1}</span><h3>{title}</h3><p>{text}</p></article>)}</div></div></section>
    <section className="section section-muted"><div className="container"><div className="section-heading"><p className="eyebrow">مزیت رقابتی</p><h2>فراتر از CRM و ارسال انبوه.</h2><p>این پنج قابلیت، فاصلهٔ نبض با ابزارهای عمومی باشگاه مشتریان و کمپین‌سازها را روشن می‌کنند.</p></div><div className="card-grid differentiator-grid">{competitiveFeatures.map(([title, text], index) => <article className="feature-card differentiator-card" key={title}><span>۰{index + 1}</span><h3>{title}</h3><p>{text}</p></article>)}</div></div></section>
    <section className="section"><div className="container split-copy"><div><p className="eyebrow">کنترل در دست شما</p><h2>پیشنهاد می‌دهد، شما تصمیم می‌گیرید.</h2></div><p>هر پیشنهاد ابتدا در صف تصمیم‌ها قرار می‌گیرد. تیم شما می‌تواند پیام و دلیل آن را بررسی، تایید یا رد کند؛ بنابراین اتوماسیون با کنترل انسانی همراه می‌ماند.</p></div></section>
    <section className="closing-cta compact"><div className="container"><h2>برای فروشگاه خودتان ببینید.</h2><Link className="button" href="/request-demo">درخواست دمو</Link></div></section>

  </PageShell>;
}
