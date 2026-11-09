"use client";

import Link from "next/link";
import { useState } from "react";
import { PageShell } from "../../components/site-shell";

const flow = [
  { number: "۰۱", title: "داده وارد می‌شود", label: "داده", text: "سفارش، سبد، تعامل و مکالمه از ابزارهای فعلی شما در یک نمای مشتری جمع می‌شوند.", signal: "سبد رهاشده پس از مشاهده هزینه ارسال", output: "تصویر واقعی از وضعیت مشتری" },
  { number: "۰۲", title: "سیگنال پیدا می‌شود", label: "تحلیل", text: "نبض ریسک ریزش، حساسیت به تخفیف، ارزش سبد و سقف تماس را با هم می‌سنجد.", signal: "حساسیت به ارسال: ۱۰۰٪ · فوریت: بالا", output: "اولویت‌بندی بدون حدس" },
  { number: "۰۳", title: "اقدام پیشنهاد می‌شود", label: "تصمیم", text: "بهترین اقدام، کانال و پیام فارسی را همراه با دلیل روشن پیشنهاد می‌کند.", signal: "اقدام: ارسال رایگان · کانال: واتساپ", output: "یک تصمیم آماده بررسی" },
  { number: "۰۴", title: "نتیجه یاد می‌گیرد", label: "بازخورد", text: "تایید، رد، بازشدن و خرید ثبت می‌شود تا اعتماد به پیشنهادهای بعدی بیشتر شود.", signal: "نتیجه: خرید پس از اقدام", output: "موتور دقیق‌تر در طول زمان" },
];

const principles = ["بدون جایگزین‌کردن CRM", "بدون تخفیف کور", "با تایید انسانی", "قابل توضیح برای تیم فروش"];

export default function HowItWorksPage() {
  const [activeStep, setActiveStep] = useState(2);
  const selected = flow[activeStep];

  return <PageShell>
    <section className="page-hero workflow-hero"><div className="container"><div className="workflow-hero-copy"><p className="eyebrow">چطور کار می‌کند</p><h1>از داده‌ی پراکنده تا <em>یک حرکت روشن.</em></h1><p>نبض به‌جای ساختن یک کمپین برای همه، هر مشتری را می‌فهمد و قدم بعدی را با دلیل پیشنهاد می‌دهد.</p><div className="hero-actions"><Link className="button" href="/demo">دموی تصمیم را ببینید</Link><a className="button button-ghost" href="#journey">مسیر را قدم‌به‌قدم ببینید</a></div></div><div className="workflow-proof"><div className="proof-top"><span>نمونه تصمیم امروز</span><b>● فعال</b></div><div className="proof-customer"><span className="avatar">م</span><div><strong>مریم احمدی</strong><small>سبد رهاشده · ۲ ساعت پیش</small></div></div><div className="proof-route"><span>سیگنال</span><b>هزینه ارسال</b><i>→</i><span>اقدام</span><strong>ارسال رایگان</strong></div><p>«هر تصمیم باید به یک رفتار واقعی وصل باشد، نه فقط یک سگمنت.»</p></div></div></section>

    <section className="workflow-trust"><div className="container"><span>ساخته شده برای تصمیم‌های روزمره فروشگاه</span><div>{principles.map((principle) => <b key={principle}>{principle}</b>)}</div></div></section>

    <section className="section workflow-journey" id="journey"><div className="container"><div className="section-heading"><p className="eyebrow">مسیر تصمیم</p><h2>چهار مرحله، یک نتیجه: اقدام درست.</h2><p>هر مرحله خروجی مشخصی دارد؛ می‌توانید روی هرکدام بزنید و ببینید در عمل چه اتفاقی می‌افتد.</p></div><div className="journey-layout"><div className="journey-tabs" role="tablist" aria-label="مراحل تصمیم">{flow.map((step, index) => <button type="button" role="tab" aria-selected={activeStep === index} className={`journey-tab ${activeStep === index ? "active" : ""}`} onClick={() => setActiveStep(index)} key={step.label}><span>{step.number}</span><div><strong>{step.title}</strong><small>{step.label}</small></div><b>←</b></button>)}</div><div className="journey-detail"><div className="detail-heading"><span>{selected.label}</span><b>{selected.number}</b></div><h3>{selected.title}</h3><p>{selected.text}</p><div className="signal-card"><small>آنچه این مرحله روشن می‌کند</small><strong>{selected.signal}</strong><span>خروجی: {selected.output}</span></div><button type="button" className="text-link" onClick={() => setActiveStep((activeStep + 1) % flow.length)}>مرحله بعد را ببینید ←</button></div></div></div></section>

    <section className="section section-muted"><div className="container workflow-example"><div><p className="eyebrow">یک مثال واقعی</p><h2>همه‌ی مشتری‌ها تخفیف نمی‌خواهند.</h2><p>برای مریم، مسئله قیمت نیست؛ سبد در لحظه دیدن هزینه ارسال رها شده. نبض به‌جای سوزاندن حاشیه سود با تخفیف، همان مانع را هدف می‌گیرد.</p><Link className="button button-ghost" href="/demo">سناریوهای دیگر را ببینید</Link></div><div className="example-stack"><div><small>داده</small><strong>سبد ۸۵۰٬۰۰۰ تومانی</strong></div><div><small>تشخیص</small><strong>حساسیت بالا به هزینه ارسال</strong></div><div className="example-highlight"><small>پیشنهاد</small><strong>ارسال رایگان در واتساپ</strong><span>با دلیل، نه حدس</span></div></div></div></section>

    <section className="closing-cta compact"><div className="container"><p className="eyebrow">قدم بعدی</p><h2>حالا نوبت داده‌های شماست.</h2><p>در یک دمو ببینید نبض برای مشتری‌های واقعی فروشگاهتان چه تصمیمی می‌سازد.</p><Link className="button" href="/request-demo">درخواست دمو</Link></div></section>
  </PageShell>;
}
