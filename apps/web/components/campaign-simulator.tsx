"use client";

import { useMemo, useState } from "react";

const sample = [
  { name: "مریم", action: "ارسال رایگان", basket: 520000, confidence: .82, incentive: "shipping" },
  { name: "نیلوفر", action: "خرید اقساطی", basket: 1450000, confidence: .88, incentive: "none" },
  { name: "آوا", action: "تخفیف هدفمند", basket: 300000, confidence: .87, incentive: "discount" },
  { name: "لیلا", action: "مشتری ویژه", basket: 405000, confidence: .9, incentive: "none" },
  { name: "سحر", action: "بازگردانی مشتری", basket: 405000, confidence: 1, incentive: "winback" },
  { name: "رویا", action: "عدم ارسال", basket: 300000, confidence: .9, incentive: "hold" },
];

const toman = new Intl.NumberFormat("fa-IR");

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
    return { items, eligible, profit: eligible.reduce((total, item) => total + item.profit, 0), protected: items.filter((item) => item.held).reduce((total, item) => total + item.incentive, 0) };
  }, [margin, shipping]);

  return <section className="campaign-simulator"><div className="simulator-copy"><p className="eyebrow">شبیه‌ساز کمپین</p><h2>پیش از ارسال، سود را ببینید.</h2><p>با تغییر حاشیه سود و هزینه ارسال، محافظ سودآوری پیشنهادهای پرهزینه را نگه می‌دارد.</p><label>حاشیه سود ناخالص <b>{toman.format(margin)}٪</b><input type="range" min="10" max="70" value={margin} onChange={(event) => setMargin(Number(event.target.value))} /></label><label>هزینه ارسال رایگان <b>{toman.format(shipping)} تومان</b><input type="range" min="30000" max="200000" step="5000" value={shipping} onChange={(event) => setShipping(Number(event.target.value))} /></label></div><div className="simulator-results"><div className="sim-metrics"><div><small>قابل اجرا</small><b>{toman.format(simulation.eligible.length)} مشتری</b></div><div><small>محافظت‌شده</small><b>{toman.format(sample.length - simulation.eligible.length)} مشتری</b></div><div><small>سود پیش‌بینی‌شده</small><b>{toman.format(Math.round(simulation.profit))} تومان</b></div></div><div className="sim-items">{simulation.items.map((item) => <div className={item.held ? "sim-item held" : "sim-item"} key={item.name}><span>{item.name}</span><p>{item.action}</p><b>{item.held ? "نگه‌داشته شد" : `${toman.format(Math.round(item.profit))} تومان`}</b></div>)}</div><p className="sim-note">محاسبهٔ سمت API: <code>POST /demo/simulations</code></p></div></section>;
}
