"use client";

import Link from "next/link";
import { useState } from "react";
import { PageShell } from "../../components/site-shell";

const panels = [
  { number: "۰۱", scene: "ورود داده", title: "همه‌چیز از یک ردپا شروع می‌شود.", copy: "مریم سبدش را ساخت، هزینه ارسال را دید و رفت. نبض این لحظه را مثل یک قاب از داستان مشتری نگه می‌دارد.", bubble: "این مشتری الان به چه چیزی نیاز دارد؟", signal: "سبد رهاشده · حساسیت به ارسال", color: "gold", icon: "✦" },
  { number: "۰۲", scene: "خواندن نشانه", title: "نبض، بین خطوط را می‌خواند.", copy: "سفارش‌های قبلی، مکالمه‌ها و سقف تماس کنار هم می‌نشینند. اینجا خبری از سگمنت‌های کور و حدس‌های عمومی نیست.", bubble: "مانع خرید، قیمت نیست؛ هزینه ارسال است.", signal: "ریسک ریزش ۶۴٪ · فوریت بالا", color: "green", icon: "◌" },
  { number: "۰۳", scene: "انتخاب حرکت", title: "قهرمان داستان، یک اقدام درست است.", copy: "از میان ۹ اقدام و چند کانال، نبض همان حرکتی را انتخاب می‌کند که هم شانس خرید را بالا ببرد و هم حاشیه سود را حفظ کند.", bubble: "ارسال رایگان، نه تخفیف بیشتر.", signal: "اقدام: ارسال رایگان · کانال: واتساپ", color: "violet", icon: "→" },
  { number: "۰۴", scene: "تایید تیم", title: "شما هنوز کارگردانید.", copy: "پیشنهاد با پیام فارسی، دلیل و میزان اطمینان وارد میز کار می‌شود. تیم شما می‌تواند قبل از هر ارسال آن را تایید یا رد کند.", bubble: "دلیلش را می‌بینم؛ تایید شد.", signal: "آماده بررسی · اطمینان ۸۲٪", color: "blue", icon: "✓" },
  { number: "۰۵", scene: "بازگشت نتیجه", title: "پایان نیست؛ قسمت بعدی است.", copy: "بازشدن پیام و خرید واقعی ثبت می‌شود. هر نتیجه، قاب بعدی داستان را برای تصمیم‌های آینده دقیق‌تر می‌کند.", bubble: "این پیشنهاد جواب داد.", signal: "خرید منتسب · یادگیری فعال", color: "gold", icon: "↻" },
];

export default function HowItWorksPage() {
  const [activePanel, setActivePanel] = useState(0);
  const panel = panels[activePanel];

  function changePanel(nextPanel: number) {
    setActivePanel(Math.max(0, Math.min(panels.length - 1, nextPanel)));
  }

  return <PageShell>
    <section className="comic-hero"><div className="container"><p className="eyebrow">چطور کار می‌کند · فصل اول</p><h1>داستان هر مشتری،<br /><em>یک پایان بهتر</em> دارد.</h1><p>اسلایدر را حرکت دهید و ببینید یک رفتار ساده چطور به تصمیمی قابل‌فهم و آماده اجرا تبدیل می‌شود.</p><div className="comic-progress"><span>شروع داستان</span><input aria-label="حرکت بین قاب‌های داستان" type="range" min="0" max={panels.length - 1} value={activePanel} onChange={(event) => changePanel(Number(event.target.value))} /><span>نتیجه</span></div></div></section>

    <section className="comic-stage" id="story"><div className="container"><div className="comic-toolbar"><span>قاب {panel.number} از ۰۵</span><b>{panel.scene}</b><span>↑ برای ادامه بکشید</span></div><div className="comic-panels"><article className={`comic-panel panel-${panel.color}`}><div className="panel-number">{panel.number}</div><div className="panel-art"><span className="panel-icon">{panel.icon}</span><i /><i /><i /></div><div className="speech-bubble">{panel.bubble}</div><div className="panel-copy"><small>{panel.scene}</small><h2>{panel.title}</h2><p>{panel.copy}</p><div className="signal-strip"><span>سیگنال این قاب</span><strong>{panel.signal}</strong></div></div></article></div><div className="comic-controls"><button type="button" className="button button-ghost button-small" disabled={activePanel === 0} onClick={() => changePanel(activePanel - 1)}>← قاب قبل</button><div className="panel-dots">{panels.map((item, index) => <button aria-label={`قاب ${item.number}`} aria-current={activePanel === index} type="button" className={activePanel === index ? "active" : ""} onClick={() => changePanel(index)} key={item.number} />)}</div><button type="button" className="button button-small" disabled={activePanel === panels.length - 1} onClick={() => changePanel(activePanel + 1)}>قاب بعد →</button></div></div></section>

    <section className="section section-muted"><div className="container comic-takeaways"><div><p className="eyebrow">چیزهایی که در هر قاب ثابت می‌مانند</p><h2>محصول، داخل داستان حل شده است.</h2><p>نمای ۳۶۰ درجه مشتری، انتخاب کانال، محافظ سودآوری، دلیل روشن و کنترل انسانی دیگر صفحه‌های جدا نیستند؛ همه در همان لحظه‌ای ظاهر می‌شوند که تیم به آن‌ها نیاز دارد.</p></div><div className="takeaway-list"><div><b>۱</b><span>داده به سیگنال تبدیل می‌شود</span></div><div><b>۲</b><span>سیگنال به اقدام سودمند می‌رسد</span></div><div><b>۳</b><span>اقدام با نتیجه بهتر می‌شود</span></div></div></div></section>

    <section className="closing-cta compact"><div className="container"><p className="eyebrow">قسمت بعدی</p><h2>داستان فروشگاه شما از کجا شروع می‌شود؟</h2><p>در میز کار تصمیم‌ها را ببینید یا یک سناریوی واقعی‌نما را اجرا کنید.</p><div className="hero-actions centered-actions"><Link className="button" href="/dashboard">ورود به میز کار</Link><Link className="button button-ghost" href="/demo">اجرای دمو</Link></div></div></section>
  </PageShell>;
}
