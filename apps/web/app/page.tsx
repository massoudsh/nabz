import Link from "next/link";
import { PageShell } from "../components/site-shell";

const problems = [
  ["تخفیف کور", "تخفیف را فقط به مشتری‌ای بدهید که واقعاً برای خرید به آن نیاز دارد."],
  ["ریزش بی‌صدا", "مشتری‌های در آستانهٔ رفتن را پیش از آن‌که دیر شود پیدا کنید."],
  ["پیام بیش‌ازحد", "فرکانس ارتباط را برای هر مشتری در محدودهٔ درست نگه دارید."],
];

const steps = [
  ["۱", "داده‌های موجود", "سفارش، سبد، مکالمه و تعامل مشتری را یک‌جا می‌خواند."],
  ["۲", "سیگنال‌های واقعی", "ریسک ریزش، حساسیت به ارسال و احتمال خرید را می‌سنجد."],
  ["۳", "اقدام بعدی", "کانال، پیشنهاد و پیام مناسب همان مشتری را پیشنهاد می‌دهد."],
];

export default function HomePage() {
  return (
    <PageShell>
      <section className="hero">
        <div className="container hero-grid">
          <div>
            <p className="eyebrow">لایهٔ تصمیم برای فروشگاه‌های ایرانی</p>
            <h1>رشد فروشگاه،<br /><em>یک تصمیم بهتر</em> در هر بار.</h1>
            <p className="hero-copy">نبض داده‌های خرید، سبد و مکالمه را به بهترین حرکت بعدی تبدیل می‌کند؛ برای هر مشتری، در زمان درست.</p>
            <div className="hero-actions"><Link className="button" href="/request-demo">درخواست دسترسی آزمایشی</Link><Link className="button button-ghost" href="/how-it-works">مسیر تصمیم را ببینید</Link></div>
            <p className="subtle-line"><span /> بدون جایگزین‌کردن CRM یا ابزار ارسال پیام</p>
          </div>
          <div className="decision-preview">
            <div className="preview-title"><span>پیشنهاد امروز</span><b>۱ تصمیم آماده</b></div>
            <div className="customer-row"><span className="avatar">م</span><div><strong>مریم احمدی</strong><small>سبد رهاشده · واتساپ</small></div><span className="status-pill">ارسال رایگان</span></div>
            <p className="message">سلام مریم جان، سبدت هنوز منتظرته! امروز ارسال رایگانه، دوست داری تکمیلش کنیم؟</p>
            <p className="reason"><span /> سبد هنگام دیدن هزینه ارسال رها شده است.</p>
            <div className="preview-footer"><span>اطمینان تصمیم</span><b>۸۲٪</b></div>
          </div>
        </div>
      </section>

      <section className="trust-bar"><div className="container"><span>تصمیم شفاف، نه جعبهٔ سیاه</span><div><b>توضیح‌پذیر</b><b>فارسی‌محور</b><b>چندکاناله</b></div></div></section>

      <section className="section"><div className="container"><div className="section-heading"><p className="eyebrow">مسئلهٔ واقعی</p><h2>داده زیاد است؛<br />تصمیم درست کمیاب.</h2><p>وقتی همه یک پیام و یک تخفیف می‌گیرند، هم حاشیه سود می‌سوزد و هم تجربه مشتری آسیب می‌بیند.</p></div><div className="card-grid">{problems.map(([title, text], index) => <article className="feature-card" key={title}><span>۰{index + 1}</span><h3>{title}</h3><p>{text}</p></article>)}</div></div></section>

      <section className="section section-muted"><div className="container"><div className="section-heading"><p className="eyebrow">از داده تا اقدام</p><h2>هر تصمیم، قابل‌فهم و آمادهٔ اجرا.</h2></div><div className="steps">{steps.map(([number, title, text]) => <article key={number}><span>{number}</span><h3>{title}</h3><p>{text}</p></article>)}</div></div></section>

      <section className="closing-cta"><div className="container"><p className="eyebrow">قدم بعدی</p><h2>فروشگاهتان را با<br /><em>تصمیم بهتر</em> رشد دهید.</h2><p>ببینید نبض با داده‌های فروشگاه شما چه تصمیم‌هایی می‌سازد.</p><Link className="button" href="/request-demo">درخواست دمو</Link></div></section>
    </PageShell>
  );
}
