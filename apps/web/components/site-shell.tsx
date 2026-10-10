import Link from "next/link";

const navigation = [
  { href: "/product", label: "محصول" },
  { href: "/how-it-works", label: "چطور کار می‌کند" },
  { href: "/demo", label: "دموی موتور" },
  { href: "/pricing", label: "پلن‌ها" },
];

export function Brand() {
  return (
    <Link className="brand" href="/" aria-label="صفحه اصلی نبض">
      <span className="brand-mark" aria-hidden="true" />
      <span>نبض</span>
    </Link>
  );
}

export function Header() {
  return (
    <header className="site-header">
      <div className="container nav">
        <Brand />
        <nav className="nav-links" aria-label="ناوبری اصلی">
          {navigation.map((item) => <Link key={item.href} href={item.href}>{item.label}</Link>)}
        </nav>
        <Link className="button button-small" href="/request-demo">درخواست دمو</Link>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-content">
        <Brand />
        <p>نبض، تصمیم بعدی هر مشتری را روشن می‌کند.</p>
        <span>© ۱۴۰۵ نبض</span>
      </div>
    </footer>
  );
}

export function PageShell({ children }: Readonly<{ children: React.ReactNode }>) {
  return <><Header /><main>{children}</main><Footer /></>;
}
