import type { CSSProperties, ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import styles from "@/app/landing.module.css";
import { AnnouncementBar, SiteFooter, SiteHeader, type NavKey } from "@/components/landing/SiteChrome";
import { AosInit } from "@/components/landing/AosInit";
import {
  IconArrowRight, IconCheck, IconChevronRight, IconHeadset, IconInfinity, IconMinus, IconPlus, IconSend, IconShield, IconTimer,
} from "@/components/brand/icons";
import { getSiteContact, planHref, planPerks, shortPrice, type Plan } from "@/lib/marketing";

/** Page frame shared by every marketing page: announcement, nav, bordered content rail and footer. */
export async function MarketingPage({ current, children }: { current?: NavKey; children: ReactNode }) {
  const { footer, waLink } = await getSiteContact();
  return (
    <main className={styles.page}>
      <AosInit />
      <a className={styles.skip} href="#konten">Lewati navigasi</a>
      <AnnouncementBar />
      <SiteHeader current={current} />
      <div className={styles.rail} id="konten">{children}</div>
      <SiteFooter copyright={footer.copyright} instagram={footer.instagram} whatsappHref={waLink} />
    </main>
  );
}

export function Breadcrumb({ items }: { items: [string, string?][] }) {
  return (
    <nav className={styles.breadcrumb} aria-label="Breadcrumb">
      {items.map(([label, href], index) => (
        <span key={label}>
          {index > 0 && <IconChevronRight size={12} aria-hidden />}
          {href ? <Link href={href}>{label}</Link> : <b aria-current="page">{label}</b>}
        </span>
      ))}
    </nav>
  );
}

/** Two-tone headline: sans line in brand orange, mono line in ink. */
export function SplitTitle({ lead, mono, as: Tag = "h2", className, id }: { lead: string; mono: string; as?: "h1" | "h2"; className?: string; id?: string }) {
  return <Tag id={id} className={`${styles.splitTitle} ${className ?? ""}`}><span>{lead}</span> <span>{mono}</span></Tag>;
}

export function EventSignup({ label = "Buat gratis" }: { label?: string }) {
  const id = `event-${label.toLowerCase().replace(/\s+/g, "-")}`;
  return (
    <form className={styles.signup} action="/auth/register" method="get">
      <label htmlFor={id} className="sr-only">Nama acaramu</label>
      <input id={id} name="event" placeholder="Nama acaramu, mis. Rina & Bima" autoComplete="off" />
      <button type="submit" className={styles.btnPrimary}>{label}</button>
    </form>
  );
}

export const defaultSteps: [string, string][] = [
  ["Pilih tema", "Jelajahi tema, lihat demo langsung, lalu pilih yang paling kamu banget."],
  ["Isi data acara", "Masukkan nama, tanggal, lokasi, foto, dan cerita kalian. Pratinjau berubah seketika."],
  ["Kirim & pantau", "Bagikan ke tamu lewat WhatsApp dan pantau RSVP serta ucapan secara real-time."],
];

export function StepsSection() {
  return (
    <section className={`${styles.section} ${styles.surface}`} id="cara-kerja" aria-labelledby="steps-title">
      <div className={styles.steps}>
        <div className={styles.titleGroup}>
          <p className={styles.eyebrow}>Cara kerja</p>
          <h2 id="steps-title" className={styles.sectionTitle}>Siap kirim dalam tiga langkah.</h2>
          <p className={styles.lead}>Tidak perlu desainer, tidak perlu laptop. Semua bisa dari HP sambil menunggu fitting baju.</p>
          <Link href="/auth/register" className={styles.btnPrimary}>Mulai buat undangan <IconArrowRight size={14} /></Link>
        </div>
        <ol className={styles.stepList}>
          {defaultSteps.map(([title, desc], index) => (
            <li key={title} data-aos="fade-up" data-aos-delay={index * 60}><b>{String(index + 1).padStart(2, "0")}</b><div><h3>{title}</h3><p>{desc}</p></div></li>
          ))}
        </ol>
      </div>
    </section>
  );
}

export function PricingPlans({ plans, waLink }: { plans: Plan[]; waLink?: string }) {
  const featuredIndex = plans.length >= 3 ? 1 : plans.length - 1;
  return <>
    <div className={styles.plans} style={{ "--plans": plans.length } as CSSProperties}>
      {plans.map((plan, index) => {
        const featured = index === featuredIndex && plans.length > 1;
        const price = shortPrice(plan.price);
        return (
          <article key={plan.id} className={`${styles.plan} ${featured ? styles.planFeatured : ""}`}>
            {featured && <div className={styles.planRibbon}>✦ PALING DIPILIH</div>}
            <div className={styles.planHead}>
              <h3>{plan.name}</h3>
              <p>{plan.price <= 0 ? "Untuk mencoba & acara sederhana." : featured ? "Paling dipilih untuk pernikahan." : "Lebih lengkap untuk acara besar."}</p>
              <div className={styles.price}>
                {price.unit && <small>{price.unit}</small>}<strong>{price.value}</strong>
                <span>{plan.price > 0 ? "sekali bayar" : "tanpa biaya"}</span>
              </div>
              <Link href={planHref(plan)} className={featured ? styles.btnPrimary : styles.btnOutline}>{plan.price > 0 ? `Pilih ${plan.name}` : "Mulai gratis"}</Link>
            </div>
            <div className={styles.planBody}>
              <p>{index === 0 ? "Yang kamu dapat" : `Semua di ${plans[index - 1].name}, plus`}</p>
              <ul>{planPerks(plan).map(perk => <li key={perk}><IconCheck size={14} strokeWidth={2.4} />{perk}</li>)}</ul>
            </div>
          </article>
        );
      })}
    </div>
    <div className={styles.assurance}>
      <b>Semua paket:</b>
      <span><IconInfinity size={16} /> Revisi sepuasnya</span>
      <span><IconSend size={16} /> Kirim via WhatsApp</span>
      <span><IconShield size={16} /> Garansi 7 hari uang kembali</span>
      <a href={waLink ?? "/tentang#kontak"} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}>Vendor WO? Program reseller <IconArrowRight size={14} /></a>
    </div>
  </>;
}

export const faqs: [string, string][] = [
  ["Apakah bisa mencoba gratis?", "Bisa. Kamu dapat membuat dan melihat pratinjau undangan tanpa biaya. Pembayaran hanya diperlukan saat undangan siap dibagikan ke tamu."],
  ["Apakah ada batas jumlah tamu?", "Setiap paket punya kapasitas tamu yang berbeda. Lihat detailnya di halaman harga sebelum memilih paket."],
  ["Berapa lama proses pembuatannya?", "Rata-rata sekitar 10 menit: pilih tema, isi data acara, lalu bagikan link ke tamu."],
  ["Apa maksud masa aktif undangan?", "Masa aktif adalah lama link undanganmu bisa dibuka tamu. Setelah lewat, kamu tetap bisa memperpanjang dari dashboard."],
  ["Apakah tema bisa di-custom?", "Bisa. Ubah foto, warna, teks, musik, dan urutan bagian undangan, lalu lihat pratinjaunya seketika."],
  ["Apakah tersedia program reseller?", "Ya. Vendor WO dan EO bisa menghubungi tim kami lewat WhatsApp untuk informasi program reseller."],
];

export function FaqSection({ waLink, items = faqs }: { waLink?: string; items?: [string, string][] }) {
  return (
    <section className={styles.section} id="faq" aria-labelledby="faq-title">
      <div className={styles.faq}>
        <div className={styles.titleGroup}>
          <p className={styles.eyebrow}>FAQ</p>
          <h2 id="faq-title" className={styles.sectionTitle}>Pertanyaan yang sering muncul.</h2>
          <p className={styles.lead}>Masih ragu? Tim kami siap bantu lewat WhatsApp setiap hari, 08.00–22.00.</p>
          <a href={waLink ?? "/tentang#kontak"} className={styles.btnOutline} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}>Chat tim support <IconArrowRight size={14} /></a>
        </div>
        <div className={styles.faqList}>
          {items.map(([question, answer], index) => (
            <details key={question} open={index === 0}>
              <summary>{question}<span className={styles.faqToggle} aria-hidden><IconPlus className={styles.plus} size={16} /><IconMinus className={styles.minus} size={16} /></span></summary>
              <p>{answer}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}

export function FinalCta({ heading, subheading }: { heading?: string; subheading?: string }) {
  return (
    <section className={`${styles.section} ${styles.surface} ${styles.cta}`} id="kontak" aria-labelledby="cta-title">
      <div className={styles.titleGroup}>
        <p className={styles.eyebrow}>Mulai sekarang</p>
        <h2 id="cta-title" className={styles.ctaTitle}>
          {heading ? <span style={{ color: "var(--rw-ink)" }}>{heading}</span> : <><span>Tamu menunggu kabar bahagiamu.</span><span>Kirim undangannya hari ini.</span></>}
        </h2>
        {subheading && <p className={styles.lead}>{subheading}</p>}
        <EventSignup label="Buat sekarang" />
        <div className={styles.trust}>
          <span><IconShield size={14} /> Pembayaran aman</span>
          <span><IconTimer size={14} /> Siap dalam 10 menit</span>
          <span><IconHeadset size={14} /> Dibantu tim support</span>
        </div>
      </div>
      <div className={styles.ctaVisual} aria-hidden>
        <Image src="/rawuh/cta-photo.webp" alt="" fill sizes="(max-width: 900px) 100vw, 480px" />
        <div className={styles.sentCard}>
          <div>Undangan terkirim<span>600 / 600</span></div>
          <div className={styles.bar}><i style={{ width: "100%" }} /></div>
          <small>Dibuka 512 tamu · 248 RSVP hadir</small>
        </div>
      </div>
    </section>
  );
}
