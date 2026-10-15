import type { CSSProperties } from "react";
import Image from "next/image";
import Link from "next/link";
import { CountUp, MotionInit } from "@/components/landing/Motion";
import { AnnouncementBar, SiteFooter, SiteHeader } from "@/components/landing/SiteChrome";
import { EventSignup, FaqSection, FinalCta, PricingPlans, StepsSection } from "@/components/landing/Sections";
import { getJSON, getLandingContent, getPlans, getProducts, getTemplates, templateDemoHref, templatePreview, type Feature, type Hero, type Kontak, type FooterContent, type Testimonial } from "@/lib/marketing";
import { ThemeGallery, VoiceWall, type Voice } from "@/components/landing/TemplateInteractions";
import {
  IconArrowRight, IconCalendar, IconGift, IconGlobe, IconImages, IconLink, IconLock, IconMusic, IconPause, IconPin, IconQrArt, IconSend, IconSparkle, IconUsers,
} from "@/components/brand/icons";

/** Admin features store an emoji; pick a matching line icon so cards match the design system. */
function FeatureIcon({ title, size = 20 }: { title: string; size?: number }) {
  const t = title.toLowerCase();
  if (/amplop|hadiah|gift|kado/.test(t)) return <IconGift size={size} />;
  if (/whatsapp|bagikan|kirim|share/.test(t)) return <IconSend size={size} />;
  if (/galeri|foto|video/.test(t)) return <IconImages size={size} />;
  if (/musik|lagu/.test(t)) return <IconMusic size={size} />;
  if (/peta|lokasi|maps/.test(t)) return <IconPin size={size} />;
  if (/tamu|guest/.test(t)) return <IconUsers size={size} />;
  if (/acara|jadwal|hitung|tanggal/.test(t)) return <IconCalendar size={size} />;
  if (/domain|link|website/.test(t)) return <IconGlobe size={size} />;
  return <IconSparkle size={size} />;
}

/** Illustration for an admin-managed feature card, matching the fixed bento cards. */
function FeatureVisual({ title }: { title: string }) {
  const t = title.toLowerCase();
  if (/amplop|hadiah|gift|kado/.test(t)) {
    return (
      <div className={styles.giftList}>
        {[["BCA", "Transfer bank", "Rp500.000"], ["GoPay", "E-wallet", "Rp250.000"], ["QRIS", "Scan QR", "Rp1.000.000"]].map(([label, kind, amount]) => (
          <div key={label} className={styles.giftRow}>
            <span className={styles.giftBadge}>{label}</span>
            <span>{kind}</span>
            <b>{amount}</b>
          </div>
        ))}
      </div>
    );
  }
  if (/whatsapp|bagikan|kirim|share/.test(t)) {
    return (
      <div className={styles.waChat}>
        <div className={styles.waBubble}>
          <p>Halo <b>Pak Budi</b>, dengan hormat kami mengundang Bapak sekeluarga 🙏</p>
          <div className={styles.waLink}><IconLink size={14} /><span>rawuh.id/rina-bima?to=Pak+Budi</span></div>
          <time>09.41 ✓✓</time>
        </div>
      </div>
    );
  }
  return <div className={styles.featureIconLg}><FeatureIcon title={title} size={28} /></div>;
}
import styles from "./landing.module.css";

const sampleVoices: Voice[] = [
  { id: "s-dinda", name: "Dinda & Arif", role: "Pernikahan · Bandung", messages: ["Kak, undangannya udah kesebar ke 600 tamu 😭", "Hemat 4 juta dari cetak, makasih banyak!"], time: "19.42", isSample: true },
  { id: "s-hasan", name: "Keluarga Hasan", role: "Aqiqah · Depok", messages: ["RSVP 3 sesi langsung kepisah otomatis. Ibu saya juga bisa ngecek sendiri 👍"], time: "08.15", isSample: true },
  { id: "s-sinar", name: "PT Sinar Abadi", role: "Acara Kantor · Jakarta", messages: ["1.200 karyawan check-in pakai QR, antrian lobby hilang total."], time: "10.27", isSample: true },
  { id: "s-nadia", name: "Nadia Amalia", role: "Ulang Tahun · Surabaya", messages: ["8 menit jadi, lagunya bisa custom!!", "Temen-temen pada nanya bikin di mana 😆"], time: "21.03", isSample: true },
  { id: "s-fajar", name: "Fajar & Rara", role: "Pernikahan · Yogyakarta", messages: ["Custom domain-nya bikin undangan terasa eksklusif ✨"], time: "14.50", isSample: true },
  { id: "s-raka", name: "Bu Ratna", role: "Khitan · Solo", messages: ["Tamu tinggal klik link, lokasi langsung kebuka di Maps. Praktis banget."], time: "16.08", isSample: true },
];

export default async function Home() {
  const [hero, kontak, footer, featuresResult, testimonialsResult, templates, plans, landing, products] = await Promise.all([
    getJSON<Hero>("/api/public/site-content/hero", {}),
    getJSON<Kontak>("/api/public/site-content/kontak", {}),
    getJSON<FooterContent>("/api/public/site-content/footer", {}),
    getJSON<{ items?: Feature[] }>("/api/public/features", {}),
    getJSON<{ items?: Testimonial[] }>("/api/public/testimonials", {}),
    getTemplates(),
    getPlans(),
    getLandingContent(),
    getProducts(),
  ]);

  // Admin-managed features render under the bento; skip ones the fixed cards above already cover.
  const builtIn = /rsvp|qr|check-?in|musik|domain|kirim sekali/i;
  const extraFeatures = (featuresResult.items ?? []).filter(feature => !builtIn.test(feature.title));
  const extraSpan = extraFeatures.length > 0 && extraFeatures.length < 3 ? 6 / extraFeatures.length : 2;
  const realVoices: Voice[] = (testimonialsResult.items ?? []).map(item => ({
    id: item.id, name: item.name, role: item.role, messages: [item.quote], isSample: item.is_sample,
  }));
  const voices = [...realVoices, ...sampleVoices.slice(0, Math.max(0, 6 - realVoices.length))];
  const waLink = kontak.whatsapp ? `https://wa.me/${kontak.whatsapp.replace(/[^0-9]/g, "")}` : undefined;
  const heroCta = hero.cta_href && hero.cta_label;

  return (
    <main className={styles.page}>
      <MotionInit />
      <a className={styles.skip} href="#konten">Lewati navigasi</a>
      <AnnouncementBar announcement={landing.announcement} />
      <SiteHeader />

      <div className={styles.rail} id="konten">
        {/* Hero */}
        <section className={styles.hero} aria-labelledby="hero-title" data-noreveal>
          <Link href="/produk/video-ucapan-3d" className={styles.pill}><b>BARU</b> Undangan Video 3D sudah hadir <IconArrowRight size={14} /></Link>
          <h1 id="hero-title" className={styles.heroTitle}>
            {hero.heading ? <span>{hero.heading}</span> : <><span>Undangan yang</span><span>terasa personal.</span></>}
          </h1>
          <p className={styles.lead}>{hero.subheading ?? "Buat undangan website dalam 10 menit dari HP. Kirim ke ratusan tamu, masing-masing dengan namanya."}</p>
          {heroCta ? <a href={hero.cta_href} className={styles.btnPrimary}>{hero.cta_label}</a> : <EventSignup />}
          <div className={styles.proof}>
            <div className={styles.avatars} aria-hidden>
              {[["D", "#2E43B0"], ["R", "#9CAF88"], ["N", "#C9A66B"], ["F", "#322F2D"]].map(([letter, color]) => <span key={letter} style={{ background: color }}>{letter}</span>)}
            </div>
            Dipakai 120.000+ pasangan &amp; keluarga
          </div>
          <div className={styles.phoneFan} aria-hidden>
            <div className={`${styles.phone} ${styles.phoneLeft}`}><Image src="/rawuh/phone-senja.webp" alt="" fill sizes="240px" preload /></div>
            <div className={`${styles.phone} ${styles.phoneCenter}`}><Image src="/rawuh/phone-kirana.webp" alt="" fill sizes="240px" preload /></div>
            <div className={`${styles.phone} ${styles.phoneRight}`}><Image src="/rawuh/phone-lentera.webp" alt="" fill sizes="240px" preload /></div>
            <span className={`${styles.chip} ${styles.chipLeft}`}><i />248 tamu hadir</span>
            <span className={`${styles.chip} ${styles.chipRight}`}><IconSend size={14} />600 undangan terkirim</span>
          </div>
        </section>

        {/* Stats */}
        <section className={styles.stats} aria-label="Rawuh dalam angka">
          {landing.stats.map(({ value, label }) => (
            <div key={value} className={styles.stat}><strong><CountUp value={value} /></strong><p>{label}</p></div>
          ))}
        </section>

        <div className={styles.banner} aria-label="Semua acaramu, satu link">
          <div className={styles.marquee} aria-hidden>
            {Array.from({ length: 2 }, (_, copy) => ["Semua acaramu, satu link", "Pernikahan", "Khitan", "Aqiqah", "Ulang tahun", "Syukuran"].map(text => <span key={`${copy}-${text}`}>{text === "Semua acaramu, satu link" && <IconLink size={16} />}{text}</span>))}
          </div>
        </div>

        {/* Features */}
        <section className={`${styles.section} ${styles.surface}`} id="fitur" aria-labelledby="fitur-title">
          <div className={styles.features}>
            <div className={styles.sectionHeader}>
              <div className={styles.titleGroup}>
                <p className={styles.eyebrow}>Fitur</p>
                <h2 id="fitur-title" className={styles.sectionTitle}>Semua yang kamu butuhkan untuk hari yang tak terulang.</h2>
              </div>
              <p className={styles.lead}>Dari kirim undangan sampai tamu datang — satu dashboard, tanpa spreadsheet.</p>
            </div>
            <div className={styles.bento}>
              <article className={`${styles.card} ${styles.cardWide}`}>
                <div className={styles.cardVisual} aria-hidden>
                  <div className={styles.sendList}>
                    {[["Budi Santoso", "Terkirim", ""], ["Keluarga Pak RT", "Dibaca", "info"], ["Sinta & suami", "Terkirim", ""], ["Om Hendra", "Mengirim…", "warn"]].map(([name, status, tone]) => (
                      <div key={name} className={styles.sendRow}>
                        <span className={styles.av}>{name[0]}</span><span>{name}</span>
                        <span className={styles.status} data-tone={tone || undefined}><i />{status}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className={styles.cardCopy}><h3>Kirim sekali klik</h3><p>Ratusan tamu, masing-masing dengan namanya — langsung lewat WhatsApp.</p></div>
              </article>
              <article className={`${styles.card} ${styles.cardDark}`}>
                <div className={`${styles.cardVisual} ${styles.rsvpCount}`} aria-hidden>
                  <strong>248</strong><span>dari 320 tamu konfirmasi hadir</span>
                  <div className={styles.bar}><i style={{ width: "78%" }} /></div>
                </div>
                <div className={styles.cardCopy}><h3>RSVP real-time</h3><p>Pantau siapa yang hadir, jumlah tamu, dan pesan menu.</p></div>
              </article>
              <article className={styles.card}>
                <div className={styles.cardVisual} aria-hidden><div className={styles.qrBox}><IconQrArt /></div></div>
                <div className={styles.cardCopy}><h3>QR Check-in</h3><p>Scan di pintu masuk, daftar hadir terisi otomatis.</p></div>
              </article>
              <article className={styles.card}>
                <div className={styles.cardVisual} aria-hidden>
                  <div className={styles.player}>
                    <span className={styles.play}><IconPause size={16} /></span>
                    <span className={styles.wave}>{[10, 18, 26, 14, 30, 22, 12, 24, 28, 16, 8, 20, 26, 12, 18, 10, 22, 14].map((h, i) => <i key={i} style={{ height: h }} data-on={i < 8 ? "" : undefined} />)}</span>
                  </div>
                </div>
                <div className={styles.cardCopy}><h3>Musik latar</h3><p>Ratusan lagu, atau unggah lagu kalian sendiri.</p></div>
              </article>
              <article className={styles.card}>
                <div className={styles.cardVisual} aria-hidden><div className={styles.url}><IconLock size={14} /><b>rinadanbima</b><span>.id</span></div></div>
                <div className={styles.cardCopy}><h3>Domain pribadi</h3><p>Alamat undangan atas nama kalian sendiri.</p></div>
              </article>
              {extraFeatures.map((feature) => (
                <article key={feature.id} className={`${styles.card} ${styles.cardExtra}`} style={{ "--span": extraSpan } as CSSProperties}>
                  <div className={styles.cardVisual} aria-hidden><FeatureVisual title={feature.title} /></div>
                  <div className={styles.cardCopy}><h3>{feature.title}</h3><p>{feature.description}</p></div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* Themes */}
        <section className={styles.section} id="tema" style={{ paddingBottom: 0 }}>
          <ThemeGallery clip templates={templates.map(template => ({
            id: template.id, name: template.name, category: template.category || "Umum",
            preview: templatePreview(template), href: `/templates/${template.slug}`,
            demoHref: templateDemoHref(template),
            isPremium: template.is_premium,
          }))} />
        </section>

        <StepsSection />

        {/* Pricing */}
        <section className={styles.section} id="harga" aria-labelledby="harga-title">
          <div className={styles.pricing}>
            <div className={styles.titleGroup}>
              <p className={styles.eyebrow}>Harga</p>
              <h2 id="harga-title" className={styles.pricingTitle}><span>Sekali bayar, </span><span>tanpa langganan.</span></h2>
              <p className={styles.pricingDesc}>Hemat hingga 90% dibanding undangan cetak. Bayar hanya saat undangan siap dikirim.</p>
            </div>
            <PricingPlans plans={plans} waLink={waLink} />
          </div>
        </section>

        {/* Testimonials */}
        <section className={`${styles.section} ${styles.surface} ${styles.voices}`} id="testimoni" aria-labelledby="voices-title">
          <div className={styles.titleGroup}>
            <p className={styles.eyebrow}>Kata mereka</p>
            <h2 id="voices-title" className={styles.sectionTitle}>Langsung dari chat pengguna kami.</h2>
          </div>
          <VoiceWall voices={voices} photos={[
            { src: "/rawuh/story-checkin.webp", caption: "QR Check-in · 312 tamu", afterIndex: 0 },
            { src: "/rawuh/story-birthday.webp", caption: "Tema Ceria", afterIndex: 3 },
            { src: "/rawuh/story-khitan.webp", caption: "Khitanan · Tema Arunika", afterIndex: 2 },
          ]} />
          <a href={waLink ?? "/tentang#kontak"} className={`${styles.btnOutline} ${styles.voicesMore}`} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}>Ceritakan pengalamanmu</a>
        </section>

        <FaqSection waLink={waLink} items={landing.faq} />
        <FinalCta heading={kontak.heading} subheading={kontak.subheading} />
      </div>

      <SiteFooter products={products} tagline={footer.tagline} copyright={footer.copyright} instagram={footer.instagram} tiktok={footer.tiktok} whatsappHref={waLink} />
    </main>
  );
}
