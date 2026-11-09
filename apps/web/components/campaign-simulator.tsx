"use client";

import { useMemo, useState } from "react";

const sample = [
  { name: "مریم", action: "ارسال رایگان", basket: 520000, confidence: .82, incentive: "shipping", channel: "واتساپ", icon: "🚚", color: "coral" },
  { name: "نیلوفر", action: "خرید اقساطی", basket: 1450000, confidence: .88, incentive: "none", channel: "دایرکت", icon: "💳", color: "violet" },
  { name: "آوا", action: "تخفیف هدفمند", basket: 300000, confidence: .87, incentive: "discount", channel: "دایرکت", icon: "🎯", color: "blue" },
  { name: "لیلا", action: "مشتری ویژه", basket: 405000, confidence: .9, incentive: "none", channel: "واتساپ", icon: "⭐", color: "gold" },
  { name: "سحر", action: "بازگردانی مشتری", basket: 405000, confidence: 1, incentive: "winback", channel: "پیامک", icon: "↩", color: "green" },
  { name: "رویا", action: "عدم ارسال", basket: 300000, confidence: .9, incentive: "hold", channel: "واتساپ", icon: "🛡", color: "slate" },
];

const toman = new Intl.NumberFormat("fa-IR");
const percent = new Intl.NumberFormat("fa-IR", { maximumFractionDigits: 1 });

export function CampaignSimulator() {
  const [margin, setMargin] = useState(35);
  const [shipping, setShipping] = useState(75000);
  const simulation = useMemo(() => {
    const items = sample.map((customer) => {
      const incentive = customer.incentive === "shipping" ? shipping : customer.incentive === "discount" ? customer.basket * .1 : customer.incentive === "winback" ? customer.basket * .15 : 0;
      const profit = customer.basket * customer.confidence * (margin / 100) - incentive;
      const held = customer.incentive === "hold" || profit < 0;
      return { ...customer, incentive, profit, held };
    });
    const eligible = items.filter((item) => !item.held);
    const revenue = eligible.reduce((total, item) => total + item.basket * item.confidence, 0);
    const spend = eligible.reduce((total, item) => total + item.incentive, 0);
    const profit = eligible.reduce((total, item) => total + item.profit, 0);
    return { items, eligible, revenue, spend, profit, protected: items.filter((item) => item.held).reduce((total, item) => total + item.incentive, 0) };
  }, [margin, shipping]);
  const reach = (simulation.eligible.length / sample.length) * 100;
  const roi = simulation.spend ? (simulation.profit / simulation.spend) * 100 : 0;
  const channelCounts = sample.reduce<Record<string, number>>((counts, item) => ({ ...counts, [item.channel]: (counts[item.channel] || 0) + 1 }), {});

  return <section className="campaign-simulator">
    <div className="simulator-copy">
      <div className="simulator-title"><span className="simulator-orb">✦</span><div><p className="eyebrow">شبیه‌ساز کمپین</p><h2>پیش از ارسال، نتیجه را ببینید.</h2></div></div>
      <p>داده‌های شش سناریوی واقعی‌نما را کنار هم می‌گذارد تا اثر هر پیشنهاد روی درآمد و حاشیه سود روشن باشد.</p>
      <label>حاشیه سود ناخالص <b>{toman.format(margin)}٪</b><input type="range" min="10" max="70" value={margin} onChange={(event) => setMargin(Number(event.target.value))} /></label>
      <label>هزینه ارسال رایگان <b>{toman.format(shipping)} تومان</b><input type="range" min="30000" max="200000" step="5000" value={shipping} onChange={(event) => setShipping(Number(event.target.value))} /></label>
      <div className="sim-source"><span>●</span><p><b>اتصال داده فعال</b><br />سفارش، رفتار و کانال ترجیحی مشتری</p></div>
    </div>
    <div className="simulator-results">
      <div className="sim-metrics">
        <div className="metric-reach"><small>پوشش کمپین</small><b>{percent.format(reach)}٪</b><span>از {toman.format(sample.length)} مشتری</span></div>
        <div className="metric-revenue"><small>درآمد قابل انتظار</small><b>{toman.format(Math.round(simulation.revenue))}</b><span>تومان</span></div>
        <div className="metric-profit"><small>سود خالص پیش‌بینی</small><b>{toman.format(Math.round(simulation.profit))}</b><span>تومان</span></div>
        <div className="metric-roi"><small>بازده پیشنهادها</small><b>{percent.format(roi)}٪</b><span>نسبت سود به مشوق</span></div>
      </div>
      <div className="sim-journey"><div className="journey-step"><strong>{toman.format(sample.length)}</strong><small>کل مخاطبان</small></div><i>←</i><div className="journey-step active"><strong>{toman.format(simulation.eligible.length)}</strong><small>پیشنهاد قابل اجرا</small></div><i>←</i><div className="journey-step safe"><strong>{toman.format(sample.length - simulation.eligible.length)}</strong><small>حفاظت‌شده</small></div></div>
      <div className="sim-insights"><div><span className="insight-icon">◈</span><p><b>محافظ سود</b><small>{toman.format(Math.round(simulation.protected))} تومان هزینه بالقوه کنترل شد</small></p></div><div><span className="insight-icon channel-icon">⌁</span><p><b>اتصال کانال</b><small>{Object.entries(channelCounts).map(([channel, count]) => `${channel} ${count}`).join(" · ")}</small></p></div></div>
      <div className="sim-items">{simulation.items.map((item) => <div className={item.held ? "sim-item held" : "sim-item"} key={item.name}><span className={`sim-avatar ${item.color}`}>{item.icon}</span><div><strong>{item.name}</strong><p>{item.action} · {item.channel}</p></div><b>{item.held ? "نگه‌داشته شد" : `${toman.format(Math.round(item.profit))} تومان`}</b></div>)}</div>
      <p className="sim-note">محاسبه بر اساس دادهٔ متصل سناریوها · <code>POST /demo/simulations</code></p>
    </div>
  </section>;
}
