"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { PageShell } from "../../components/site-shell";

const channels = [
  { id: "all", label: "همه کانال‌ها", count: 24 },
  { id: "whatsapp", label: "واتساپ", count: 9 },
  { id: "instagram", label: "اینستاگرام", count: 8 },
  { id: "sms", label: "پیامک", count: 7 },
];

const actions = [
  { id: 1, channel: "whatsapp", channelLabel: "واتساپ", initial: "م", name: "مریم احمدی", action: "ارسال رایگان", reason: "سبد پس از دیدن هزینه ارسال رها شده", confidence: 82, tone: "gold", time: "امروز، ۱۴:۳۰" },
  { id: 2, channel: "instagram", channelLabel: "اینستاگرام", initial: "آ", name: "آوا کریمی", action: "تخفیف هدفمند", reason: "در مکالمه اخیر قیمت محصول را پرسیده", confidence: 87, tone: "green", time: "امروز، ۱۵:۰۰" },
  { id: 3, channel: "whatsapp", channelLabel: "واتساپ", initial: "ن", name: "نیلوفر رضایی", action: "خرید اقساطی", reason: "سبد باارزش در مرحله پرداخت متوقف شده", confidence: 88, tone: "violet", time: "امروز، ۱۶:۱۵" },
  { id: 4, channel: "sms", channelLabel: "پیامک", initial: "س", name: "سحر اکبری", action: "پیام بازگشت", reason: "از چرخه معمول خرید فاصله گرفته", confidence: 79, tone: "blue", time: "فردا، ۱۰:۰۰" },
];

function Gauge({ value, label, caption, color }: { value: number; label: string; caption: string; color: string }) {
  return <div className="metric-gauge"><div className="gauge-ring" style={{ background: `conic-gradient(${color} ${value * 3.6}deg, rgba(255,255,255,.08) 0deg)` }}><div><strong>{value}%</strong><small>{label}</small></div></div><p>{caption}</p></div>;
}

export default function DashboardPage() {
  const [activeChannel, setActiveChannel] = useState("all");
  const [selectedId, setSelectedId] = useState(1);
  const selected = actions.find((item) => item.id === selectedId) ?? actions[0];
  const visibleActions = useMemo(() => activeChannel === "all" ? actions : actions.filter((item) => item.channel === activeChannel), [activeChannel]);

  return <PageShell>
    <section className="dashboard-page"><div className="container dashboard-shell">
      <section className="dashboard-heading"><div><p className="eyebrow">میز کار نبض</p><h1>صبح بخیر، تیم رشد.</h1><p>از یک میز، تمام کانال‌ها و تصمیم‌های امروز را مدیریت کنید.</p></div><div className="dashboard-actions"><span className="live-dot">● همگام‌سازی فعال</span><Link className="button button-small" href="/demo">اجرای دمو</Link></div></section>

      <section className="dashboard-metrics"><div className="dashboard-card metric-intro"><p className="eyebrow">نمای امروز</p><h2>تصمیم‌ها در جریان‌اند.</h2><p>نبض ۲۴ مشتری را برای اقدام بعدی آماده کرده و از هزینه‌های بی‌اثر جلوگیری کرده است.</p><Link className="text-link" href="/how-it-works">تصمیم‌ها چطور ساخته می‌شوند؟ ←</Link></div><div className="dashboard-card gauge-card"><Gauge value={82} label="اعتماد" caption="میانگین اطمینان تصمیم‌ها" color="#e8b76a" /></div><div className="dashboard-card gauge-card"><Gauge value={68} label="خرید" caption="نرخ تبدیل این هفته" color="#7ed7ad" /></div><div className="dashboard-card gauge-card"><Gauge value={91} label="سلامت" caption="رعایت حاشیه سود" color="#a99cf4" /></div></section>

      <section className="channel-desk"><div className="desk-heading"><div><p className="eyebrow">کشوی کانال‌ها</p><h2>هر کانال، یک صف روشن.</h2></div><span>آخرین بروزرسانی: همین حالا</span></div><div className="channel-tabs" role="tablist">{channels.map((channel) => <button type="button" role="tab" aria-selected={activeChannel === channel.id} className={activeChannel === channel.id ? "active" : ""} onClick={() => setActiveChannel(channel.id)} key={channel.id}><span>{channel.label}</span><b>{channel.count}</b></button>)}</div><div className="desk-grid">{visibleActions.map((item) => <button type="button" className={`action-card ${selectedId === item.id ? "selected" : ""}`} key={item.id} onClick={() => setSelectedId(item.id)}><div className="action-card-top"><span className={`channel-mark ${item.tone}`}>{item.initial}</span><span className="action-channel">{item.channelLabel}</span><small>{item.time}</small></div><strong>{item.name}</strong><b className="action-pill">{item.action}</b><p>{item.reason}</p><div className="action-confidence"><span>اطمینان</span><b>{item.confidence}%</b><i><em style={{ width: `${item.confidence}%` }} /></i></div></button>)}</div></section>

      <section className="dashboard-bottom"><div className="dashboard-card selected-decision"><div className="selected-header"><div><p className="eyebrow">تصمیم انتخاب‌شده</p><h2>{selected.name}</h2></div><span className="status-badge">آماده بررسی</span></div><div className="selected-meta"><span>{selected.channelLabel}</span><b>{selected.action}</b><span>{selected.time}</span></div><blockquote>سلام {selected.name.replace("مریم ", "").replace("آوا ", "").replace("نیلوفر ", "").replace("سحر ", "")} جان، بر اساس رفتار خریدت یک پیشنهاد مناسب برایت آماده کرده‌ایم.</blockquote><div className="selected-footer"><span>دلیل: {selected.reason}</span><div><button type="button" className="button button-small button-ghost">رد کردن</button><button type="button" className="button button-small">تایید اقدام</button></div></div></div><div className="dashboard-card mini-report"><p className="eyebrow">گزارش سریع</p><h3>اثر تصمیم‌ها</h3><div className="report-row"><span>درآمد منتسب</span><b>۱۲٫۴M</b><i className="up">+۱۸٪</i></div><div className="report-row"><span>هزینه مشوق</span><b>۲٫۱M</b><i className="down">−۹٪</i></div><div className="report-row"><span>مشتری‌های محافظت‌شده</span><b>۳۶</b><i className="up">+۱۲</i></div><Link className="text-link" href="/demo">گزارش کامل کمپین ←</Link></div></section>
    </div></section>
  </PageShell>;
}
