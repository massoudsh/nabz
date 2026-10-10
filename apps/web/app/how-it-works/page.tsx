import Link from "next/link";
import { PageShell } from "../../components/site-shell";

const flow = [
  ["داده", "اطلاعات سفارش، سبد، تعامل و مکالمه از ابزارهای فعلی شما وارد می‌شوند."],
  ["تحلیل", "نبض نشانه‌های ریسک ریزش، حساسیت به تخفیف و سقف تماس را ارزیابی می‌کند."],
  ["تصمیم", "بهترین اقدام، کانال و پیام را با دلیل شفاف پیشنهاد می‌کند."],
  ["بازخورد", "نتیجهٔ هر اقدام ثبت می‌شود تا پیشنهادهای آینده دقیق‌تر شوند."],
];

export default function HowItWorksPage() {
  return <PageShell><section className="page-hero"><div className="container narrow"><p className="eyebrow">چطور کار می‌کند</p><h1>از سیگنال مشتری تا اقدام بعدی.</h1><p>فرآیند نبض برای تیم فروش قابل‌فهم است: داده را می‌گیرد، نشانه را پیدا می‌کند و پیشنهاد قابل‌اجرا می‌دهد.</p></div></section><section className="workflow-visual"><div className="container"><img src="/how-it-works-handwritten.jpg" alt="روند داده، تحلیل، تصمیم و بازخورد در نبض" /></div></section><section className="section"><div className="container timeline">{flow.map(([title, text], index) => <article key={title}><span>{index + 1}</span><div><h2>{title}</h2><p>{text}</p></div></article>)}</div></section><section className="section section-muted"><div className="container split-copy"><div><p className="eyebrow">حریم تصمیم</p><h2>نه CRM جدید، نه پیام‌رسان جدید.</h2></div><p>نبض جای سیستم‌های فعلی شما را نمی‌گیرد. این محصول لایهٔ تصمیمی است که بین داده‌های موجود و کانال ارتباطی شما قرار می‌گیرد.</p></div></section><section className="closing-cta compact"><div className="container"><h2>برای داده‌های خودتان امتحانش کنید.</h2><Link className="button" href="/request-demo">شروع گفتگو</Link></div></section></PageShell>;
}
