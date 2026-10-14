import Link from "next/link";
import styles from "@/app/landing.module.css";
import { IconArrowRight, IconChevronDown, IconFacebook, IconHeart, IconInstagram, IconMessage, IconYoutube } from "@/components/brand/icons";
import { MobileMenu } from "./TemplateInteractions";

export function RawuhLogo({ label = "RAWUH", href = "/" }: { label?: string; href?: string }) {
  return (
    <Link href={href} className={styles.logo} aria-label="Rawuh, ke beranda">
      <IconHeart size={20} strokeWidth={2.2} />
      {label}
    </Link>
  );
}

export function AnnouncementBar() {
  return (
    <div className={styles.announcement}>
      <span>Baru: Undangan Video 3D &amp; QR Check-in untuk semua paket Premium</span>
      <Link href="/produk/video-ucapan-3d">Lihat sekarang <IconArrowRight size={14} /></Link>
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

type FooterProps = { tagline?: string; copyright?: string; instagram?: string; whatsappHref?: string };

export function SiteFooter({ tagline, copyright, instagram, whatsappHref }: FooterProps) {
  const columns = [
    { title: "Produk", links: [["Undangan Website", "/produk/undangan-website"], ["Video Ucapan 3D", "/produk/video-ucapan-3d"], ["QR Check-in", "/produk/qr-checkin"], ["Undangan Cetak", "/produk/undangan-cetak"]] },
    { title: "Acara", links: [["Pernikahan", "/templates"], ["Khitan", "/templates"], ["Aqiqah", "/templates"], ["Ulang Tahun", "/templates"], ["Syukuran", "/templates"]] },
    { title: "Perusahaan", links: [["Tentang kami", "/tentang"], ["Program Reseller", "/tentang#kontak"], ["Tim", "/tentang#tim"], ["Fitur", "/fitur"]] },
    { title: "Bantuan", links: [["Pusat bantuan", "/harga#faq"], ["Panduan membuat", "/fitur#cara-kerja"], ["Hubungi kami", whatsappHref ?? "/tentang#kontak"]] },
  ];
  const instagramHref = instagram ? `https://instagram.com/${instagram.replace(/^@/, "")}` : undefined;
  return (
    <footer className={styles.footer}>
      <div className={styles.footerInner}>
        <div className={styles.footerTop}>
          <div className={styles.footerBrand}>
            <RawuhLogo />
            <p>{tagline ?? "Undangan digital untuk setiap momen berharga. Dibuat dengan sepenuh hati di Yogyakarta."}</p>
            <div className={styles.socials}>
              {instagramHref && <a href={instagramHref} target="_blank" rel="noreferrer" aria-label="Instagram Rawuh"><IconInstagram /></a>}
              <a href="https://youtube.com" target="_blank" rel="noreferrer" aria-label="YouTube Rawuh"><IconYoutube /></a>
              <a href="https://facebook.com" target="_blank" rel="noreferrer" aria-label="Facebook Rawuh"><IconFacebook /></a>
              {whatsappHref && <a href={whatsappHref} target="_blank" rel="noreferrer" aria-label="WhatsApp Rawuh"><IconMessage /></a>}
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
            <Link href="/">Syarat &amp; Ketentuan</Link>
            <Link href="/">Kebijakan Privasi</Link>
            <span>{copyright ?? `© ${new Date().getFullYear()} Rawuh.id`}</span>
          </div>
        </div>
      </div>
      <svg className={styles.giant} viewBox="0 0 1200 250" aria-hidden="true" focusable="false">
        <text x="600" y="235" textAnchor="middle" fontSize="330" letterSpacing="-14">rawuh.</text>
      </svg>
    </footer>
  );
}
