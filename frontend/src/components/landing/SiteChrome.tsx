import Link from "next/link";
import { defaultAnnouncement, type Announcement } from "@/lib/marketing";
import { defaultProducts } from "@/lib/products";
import styles from "@/app/landing.module.css";
import { IconArrowRight, IconInstagram, IconTiktok, IconWhatsapp } from "@/components/brand/icons";
import { RawuhTile } from "@/components/brand/RawuhMark";
import { ThemeToggle } from "./ThemeToggle";
import { MobileMenu } from "./TemplateInteractions";

export function RawuhLogo({ label = "rawuh", href = "/" }: { label?: string; href?: string }) {
  return (
    <Link href={href} className={styles.logo} aria-label="Rawuh, ke beranda">
      <RawuhTile size={32} />
      {label}
    </Link>
  );
}

export function AnnouncementBar({ announcement }: { announcement?: Announcement }) {
  const item = announcement ?? defaultAnnouncement;
  if (item.enabled === false || !item.text?.trim()) return null;
  const href = item.href?.trim();
  const external = href ? /^https?:\/\//.test(href) : false;
  return (
    <div className={styles.announcement}>
      <span>{item.text}</span>
      {href && item.label?.trim() && (
        external
          ? <a href={href} target="_blank" rel="noreferrer">{item.label} <IconArrowRight size={14} /></a>
          : <Link href={href}>{item.label} <IconArrowRight size={14} /></Link>
      )}
    </div>
  );
}

export type NavKey = "tema" | "fitur" | "harga" | "tentang" | "produk" | "reseller" | undefined;

export function SiteHeader({ current }: { current?: NavKey }) {
  const links: { key: NavKey; href: string; label: string }[] = [
    { key: "tema", href: "/templates", label: "Tema" },
    { key: "fitur", href: "/fitur", label: "Fitur" },
    { key: "harga", href: "/harga", label: "Harga" },
    { key: "reseller", href: "/reseller", label: "Reseller" },
    { key: "tentang", href: "/tentang", label: "Tentang" },
  ];
  return (
    <header className={styles.header}>
      <nav className={styles.nav} aria-label="Navigasi utama">
        <RawuhLogo />
        <div className={styles.navLinks}>
          {links.map(link => (
            <Link key={link.label} href={link.href} aria-current={current === link.key ? "page" : undefined}>
              {link.label}
            </Link>
          ))}
        </div>
        <div className={styles.navActions}>
          <ThemeToggle />
          <Link href="/auth/login" className={styles.btnOutline}>Masuk</Link>
          <Link href="/auth/register" className={styles.btnPrimary}>Buat Undangan</Link>
          <MobileMenu />
        </div>
      </nav>
    </header>
  );
}

export type FooterColumn = { title: string; links: { label: string; href: string }[] };

/** Footer link columns after "Produk"; "contact" as href opens the admin WhatsApp. Admins edit them in /admin/footer. */
export const defaultFooterColumns: FooterColumn[] = [
  { title: "Acara", links: [{ label: "Pernikahan", href: "/templates" }, { label: "Khitan", href: "/templates" }, { label: "Aqiqah", href: "/templates" }, { label: "Ulang Tahun", href: "/templates" }, { label: "Syukuran", href: "/templates" }] },
  { title: "Perusahaan", links: [{ label: "Tentang kami", href: "/tentang" }, { label: "Program Reseller", href: "/reseller" }, { label: "Tim", href: "/tentang#tim" }, { label: "Fitur", href: "/fitur" }] },
  { title: "Bantuan", links: [{ label: "Pusat bantuan", href: "/harga#faq" }, { label: "Panduan membuat", href: "/fitur#cara-kerja" }, { label: "Hubungi kami", href: "contact" }] },
];
export const defaultPaymentMethods = ["QRIS", "Virtual Account", "GoPay", "OVO", "Kartu Kredit"];

type FooterProps = { columns?: FooterColumn[]; paymentMethods?: string[]; products?: { slug: string; name: string }[]; tagline?: string; copyright?: string; instagram?: string; tiktok?: string; whatsappHref?: string };

// Content saved before the rebrand may still say "Yukakad"; fall back to Rawuh defaults instead of showing it.
const legacyBrand = (value?: string) => value && !/yukakad/i.test(value) ? value : undefined;

export function SiteFooter({ columns: rawColumns, paymentMethods: rawPayments, products = defaultProducts, tagline: rawTagline, copyright: rawCopyright, instagram: rawInstagram, tiktok, whatsappHref }: FooterProps) {
  const copyright = legacyBrand(rawCopyright);
  const tagline = legacyBrand(rawTagline?.trim());
  const instagram = legacyBrand(rawInstagram);
  const columns = [
    { title: "Produk", links: products.map(product => [product.name, `/produk/${product.slug}`]) },
    ...(rawColumns?.length ? rawColumns : defaultFooterColumns).map(column => ({
      title: column.title,
      links: column.links.filter(link => link.label?.trim() && link.href?.trim()).map(link => [link.label, link.href === "contact" ? whatsappHref ?? "/tentang#kontak" : link.href]),
    })),
  ];
  const paymentMethods = rawPayments?.filter(method => method.trim()).length ? rawPayments.filter(method => method.trim()) : defaultPaymentMethods;
  const instagramHref = instagram ? `https://instagram.com/${instagram.replace(/^@/, "")}` : undefined;
  const tiktokHref = tiktok ? `https://www.tiktok.com/@${tiktok.replace(/^@/, "")}` : undefined;
  return (
    <footer className={styles.footer}>
      <div className={styles.footerInner}>
        <div className={styles.footerTop}>
          <div className={styles.footerBrand}>
            <RawuhLogo />
            <p>{tagline ?? "Undangan digital untuk setiap momen berharga. Dibuat dengan sepenuh hati di Yogyakarta."}</p>
            <div className={styles.socials}>
              {instagramHref && <a href={instagramHref} target="_blank" rel="noreferrer" aria-label="Instagram Rawuh"><IconInstagram size={18} /></a>}
              {tiktokHref && <a href={tiktokHref} target="_blank" rel="noreferrer" aria-label="TikTok Rawuh"><IconTiktok size={18} /></a>}
              {whatsappHref && <a href={whatsappHref} target="_blank" rel="noreferrer" aria-label="WhatsApp Rawuh"><IconWhatsapp size={18} /></a>}
            </div>
          </div>
          {columns.map(column => (
            <nav key={column.title} className={styles.footerCol} aria-label={column.title}>
              <p>{column.title}</p>
              {column.links.map(([label, href]) => <Link key={label} href={href}>{label}</Link>)}
            </nav>
          ))}
        </div>
        <div className={styles.footerBottom}>
          <div className={styles.payments}>Bayar via {paymentMethods.map(method => <span key={method}>{method}</span>)}</div>
          <div className={styles.legal}>
            <Link href="/syarat-ketentuan">Syarat &amp; Ketentuan</Link>
            <Link href="/kebijakan-privasi">Kebijakan Privasi</Link>
            <span>{copyright ?? `© ${new Date().getFullYear()} Rawuh.id`}</span>
          </div>
        </div>
        {/* Metrics from Be Vietnam Pro Bold at 404px: ink spans exactly 1280 wide, "h" ascender at y=0, baseline at 307. */}
        <svg className={styles.giant} viewBox="0 0 1280 312" aria-hidden="true" focusable="false">
          <text x="-23.4" y="307" fontSize="404" letterSpacing="-16.2">rawuh.</text>
        </svg>
      </div>
    </footer>
  );
}
