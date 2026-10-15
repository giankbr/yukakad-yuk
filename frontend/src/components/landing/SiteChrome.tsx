import Link from "next/link";
import { defaultAnnouncement, type Announcement } from "@/lib/marketing";
import styles from "@/app/landing.module.css";
import { IconArrowRight, IconChevronDown, IconHeart, IconInstagram, IconTiktok, IconWhatsapp } from "@/components/brand/icons";
import { MobileMenu } from "./TemplateInteractions";

export function RawuhLogo({ label = "RAWUH", href = "/" }: { label?: string; href?: string }) {
  return (
    <Link href={href} className={styles.logo} aria-label="Rawuh, ke beranda">
      <IconHeart size={20} strokeWidth={2.2} />
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

export type NavKey = "tema" | "fitur" | "harga" | "tentang" | "produk" | undefined;

export function SiteHeader({ current }: { current?: NavKey }) {
  const links: { key: NavKey; href: string; label: string; menu?: boolean }[] = [
    { key: "tema", href: "/templates", label: "Tema", menu: true },
    { key: "fitur", href: "/fitur", label: "Fitur" },
    { key: "harga", href: "/harga", label: "Harga", menu: true },
  ];
  return (
    <header className={styles.header}>
      <nav className={styles.nav} aria-label="Navigasi utama">
        <RawuhLogo />
        <div className={styles.navLinks}>
          {links.map(link => (
            <Link key={link.label} href={link.href} aria-current={current === link.key ? "page" : undefined}>
              {link.label}{link.menu && <IconChevronDown size={14} />}
            </Link>
          ))}
        </div>
        <div className={styles.navActions}>
          <Link href="/auth/login" className={styles.btnOutline}>Masuk</Link>
          <Link href="/auth/register" className={styles.btnPrimary}>Buat Undangan</Link>
          <MobileMenu />
        </div>
      </nav>
    </header>
  );
}

type FooterProps = { tagline?: string; copyright?: string; instagram?: string; tiktok?: string; whatsappHref?: string };

// Content saved before the rebrand may still say "Yukakad"; fall back to Rawuh defaults instead of showing it.
const legacyBrand = (value?: string) => value && !/yukakad/i.test(value) ? value : undefined;

export function SiteFooter({ tagline, copyright: rawCopyright, instagram: rawInstagram, tiktok, whatsappHref }: FooterProps) {
  const copyright = legacyBrand(rawCopyright);
  const instagram = legacyBrand(rawInstagram);
  const columns = [
    { title: "Produk", links: [["Undangan Website", "/produk/undangan-website"], ["Video Ucapan 3D", "/produk/video-ucapan-3d"], ["QR Check-in", "/produk/qr-checkin"], ["Undangan Cetak", "/produk/undangan-cetak"]] },
    { title: "Acara", links: [["Pernikahan", "/templates"], ["Khitan", "/templates"], ["Aqiqah", "/templates"], ["Ulang Tahun", "/templates"], ["Syukuran", "/templates"]] },
    { title: "Perusahaan", links: [["Tentang kami", "/tentang"], ["Program Reseller", "/tentang#kontak"], ["Tim", "/tentang#tim"], ["Fitur", "/fitur"]] },
    { title: "Bantuan", links: [["Pusat bantuan", "/harga#faq"], ["Panduan membuat", "/fitur#cara-kerja"], ["Hubungi kami", whatsappHref ?? "/tentang#kontak"]] },
  ];
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
          <div className={styles.payments}>Bayar via {["QRIS", "Virtual Account", "GoPay", "OVO", "Kartu Kredit"].map(method => <span key={method}>{method}</span>)}</div>
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
