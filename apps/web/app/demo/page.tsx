"use client";

import { useMemo, useState } from "react";
import { PageShell } from "../../components/site-shell";

const scenarios = [
  { id: "demo_maryam", name: "مریم احمدی", signal: "سبد رهاشده پس از دیدن هزینه ارسال", action: "ارسال رایگان", channel: "واتساپ", confidence: 82, message: "سلام مریم جان، سبدت هنوز منتظرته! امروز ارسال رایگانه، دوست داری تکمیلش کنیم؟", reason: "دو بار قبلی هنگام مشاهده هزینه ارسال، سبد رها شده است." },
  { id: "demo_niloofar", name: "نیلوفر رضایی", signal: "سبد با ارزش بالا در مرحله پرداخت", action: "پیشنهاد خرید اقساطی", channel: "دایرکت اینستاگرام", confidence: 88, message: "نیلوفر جان، پرداخت اقساطی برای این سفارش فعال است. اگر دوست داری همین حالا سفارشت را تکمیل کن.", reason: "ارزش سبد بالاتر از میانگین فروشگاه است و در مرحله پرداخت رها شده." },
  { id: "demo_ava", name: "آوا کریمی", signal: "سؤال قیمت در مکالمه اخیر", action: "تخفیف هدفمند", channel: "دایرکت اینستاگرام", confidence: 87, message: "آوا جان، برای مدلی که پرسیده بودی یک پیشنهاد ویژه داریم. دوست داری جزئیاتش را بفرستیم؟", reason: "در چهار ساعت اخیر قیمت پرسیده و پس از آن خریدی ثبت نشده است." },
  { id: "demo_leila", name: "لیلا محمدی", signal: "خرید مکرر بدون استفاده از تخفیف", action: "مشتری ویژه، بدون تخفیف", channel: "واتساپ", confidence: 90, message: "لیلا جان، محصولات تازه‌ای رسیدند که فکر می‌کنیم دوستشان داشته باشی.", reason: "مشتری وفادار است و تخفیف در سابقه خرید او نقشی نداشته است." },
  { id: "demo_sahar", name: "سحر اکبری", signal: "فاصله زیاد از چرخه معمول خرید", action: "پیام بازگشت", channel: "پیامک", confidence: 100, message: "سحر عزیز، مدتی است دلمان برایتان تنگ شده. یک پیشنهاد ویژه برای بازگشت شما آماده است.", reason: "ریسک ریزش نسبت به الگوی خرید گذشته بالا است." },
  { id: "demo_roya", name: "رویا حسینی", signal: "سقف پیام هفتگی تکمیل شده", action: "عدم ارسال پیام", channel: "واتساپ", confidence: 90, message: "", reason: "برای رعایت تجربه مشتری، این هفته پیام دیگری ارسال نمی‌شود." },
];

export default function DemoPage() {
  const [selectedId, setSelectedId] = useState(scenarios[0].id);
  const [isRun, setIsRun] = useState(false);
  const selected = useMemo(() => scenarios.find((scenario) => scenario.id === selectedId)!, [selectedId]);

  function runEngine() {
    setIsRun(false);
    window.setTimeout(() => setIsRun(true), 280);
  }

  return <PageShell><section className="page-hero demo-hero"><div className="container narrow"><p className="eyebrow">محیط آزمایشی موتور</p><h1>ببینید نبض برای هر مشتری چه تصمیمی می‌گیرد.</h1><p>این داده‌ها ساختگی‌اند، اما تصمیم‌ها با همان منطق موتور نبض ساخته شده‌اند: سیگنال، اقدام، کانال و پیام مناسب.</p></div></section><section className="section demo-section"><div className="container demo-grid"><aside className="scenario-list"><div><p className="eyebrow">۶ سناریوی نمونه</p><h2>یک مشتری را انتخاب کنید</h2></div>{scenarios.map((scenario) => <button type="button" key={scenario.id} onClick={() => { setSelectedId(scenario.id); setIsRun(false); }} className={`scenario ${selectedId === scenario.id ? "selected" : ""}`}><span>{scenario.name.slice(0, 1)}</span><div><strong>{scenario.name}</strong><small>{scenario.signal}</small></div></button>)}</aside><div className="engine-panel"><div className="engine-top"><div><p className="eyebrow">خروجی موتور تصمیم</p><h2>{selected.name}</h2></div><button className="button button-small" onClick={runEngine} type="button">اجرای موتور</button></div>{isRun ? <div className="engine-result"><div className="result-heading"><span>اقدام پیشنهادی</span><strong>{selected.action}</strong></div><div className="result-details"><div><small>کانال پیشنهادی</small><b>{selected.channel}</b></div><div><small>اطمینان موتور</small><b>{selected.confidence}٪</b></div></div>{selected.message ? <blockquote>{selected.message}</blockquote> : <div className="no-message">برای حفظ تجربه مشتری، پیام جدیدی پیشنهاد نشده است.</div>}<div className="reason-box"><span>دلیل تصمیم</span><p>{selected.reason}</p></div></div> : <div className="engine-idle"><span>◌</span><h3>آمادهٔ تحلیل</h3><p>روی «اجرای موتور» بزنید تا خروجی این سناریو را ببینید.</p></div>}<p className="api-note">برای دریافت همین داده‌ها از API: <code>GET /demo/overview</code></p></div></div></section></PageShell>;
}
