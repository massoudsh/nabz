"use client";

import { FormEvent, useState } from "react";
import { PageShell } from "../../components/site-shell";

export default function RequestDemoPage() {
  const [submitted, setSubmitted] = useState(false);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
  }

  return <PageShell><section className="page-hero"><div className="container narrow"><p className="eyebrow">درخواست دمو</p><h1>بیایید با داده‌های فروشگاه شما شروع کنیم.</h1><p>اطلاعات اولیه را بفرستید تا برای یک گفتگوی کوتاه و بررسی فرصت‌های نبض با شما هماهنگ کنیم.</p></div></section><section className="section"><div className="container form-layout"><form className="demo-form" onSubmit={submit}>{submitted ? <div className="success-box"><strong>درخواست شما ثبت شد.</strong><p>به‌زودی برای هماهنگی دمو با شما تماس می‌گیریم.</p></div> : <><label>نام و نام خانوادگی<input name="name" required placeholder="مثلاً سارا احمدی" /></label><label>ایمیل کاری<input name="email" type="email" required placeholder="you@store.ir" /></label><label>نام فروشگاه<input name="store" required placeholder="نام فروشگاه شما" /></label><label>تعداد مشتری فعال<select name="customers" defaultValue=""><option value="" disabled>یک بازه انتخاب کنید</option><option>کمتر از ۱٬۰۰۰</option><option>۱٬۰۰۰ تا ۵٬۰۰۰</option><option>بیش از ۵٬۰۰۰</option></select></label><label className="full-width">دربارهٔ فروشگاهتان<textarea name="note" rows={4} placeholder="کانال‌های فروش و مهم‌ترین مسئله‌ای که می‌خواهید حل کنید" /></label><button className="button" type="submit">ثبت درخواست</button></>}</form><aside className="form-aside"><p className="eyebrow">در دمو چه می‌بینید؟</p><h2>تصمیم‌های فروشگاه شما، نه یک نمونهٔ کلی.</h2><ul><li>نشانه‌هایی که نبض از داده‌ها می‌خواند</li><li>نمونهٔ پیشنهاد برای مشتریان مختلف</li><li>مناسب‌ترین مسیر شروع برای تیم شما</li></ul></aside></div></section></PageShell>;
}
