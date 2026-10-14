import type { CSSProperties } from "react";
import Image from "next/image";
import Link from "next/link";
import { AosInit } from "@/components/landing/AosInit";
import { AnnouncementBar, SiteFooter, SiteHeader } from "@/components/landing/SiteChrome";
import { ThemeGallery, VoiceWall, type Voice } from "@/components/landing/TemplateInteractions";
import {
  IconArrowRight, IconCheck, IconHeadset, IconInfinity, IconLink, IconLock, IconMinus, IconPause,
  IconPlus, IconQr, IconSend, IconShield, IconTimer,
} from "@/components/brand/icons";
import styles from "./landing.module.css";

const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

type Hero = { heading?: string; subheading?: string; cta_label?: string; cta_href?: string };
type Kontak = { heading?: string; subheading?: string; whatsapp?: string };
type Footer = { heading?: string; copyright?: string; instagram?: string };
type Feature = { id: string; title: string; description: string; icon?: string };
type Testimonial = { id: string; name: string; role?: string; quote: string; avatar_url?: string; is_sample?: boolean };
type Template = { id: string; name: string; slug: string; category: string; preview_image?: string; preview_url?: string; is_premium: boolean };
type Plan = { id: string; name: string; max_guests: number; has_watermark: boolean; custom_domain_allowed: boolean; payment_gateway_allowed: boolean; price: number; duration_days?: number | null };

const defaultTemplates: Template[] = [
  { id: "alyra", name: "Alyra", slug: "alyra", category: "Editorial", preview_url: "/invitation/demo?template=alyra", is_premium: false },
  { id: "weddings", name: "Weddings", slug: "weddings", category: "Modern", preview_url: "/invitation/demo?template=weddings", is_premium: false },
  { id: "veloria", name: "Veloria", slug: "veloria", category: "Editorial", preview_url: "/invitation/demo?template=veloria", is_premium: false },
];

const defaultPlans: Plan[] = [
  { id: "free", name: "Mulai", max_guests: 100, has_watermark: true, custom_domain_allowed: false, payment_gateway_allowed: false, price: 0 },
  { id: "pro", name: "Rayakan", max_guests: 1000, has_watermark: false, custom_domain_allowed: true, payment_gateway_allowed: true, price: 149000, duration_days: 30 },
];

const templateImages: Record<string, string> = {
  alyra: "/templates/alyra-preview.png",
  weddings: "/templates/weddings-preview.png",
  veloria: "/templates/veloria-preview.png",
};

const sampleVoices: Voice[] = [
  { id: "s-dinda", name: "Dinda & Arif", role: "Pernikahan · Bandung", messages: ["Kak, undangannya udah kesebar ke 600 tamu 😭", "Hemat 4 juta dari cetak, makasih banyak!"], time: "19.42", isSample: true },
  { id: "s-hasan", name: "Keluarga Hasan", role: "Aqiqah · Depok", messages: ["RSVP 3 sesi langsung kepisah otomatis. Ibu saya juga bisa ngecek sendiri 👍"], time: "08.15", isSample: true },
  { id: "s-sinar", name: "PT Sinar Abadi", role: "Acara Kantor · Jakarta", messages: ["1.200 karyawan check-in pakai QR, antrian lobby hilang total."], time: "10.27", isSample: true },
  { id: "s-nadia", name: "Nadia Amalia", role: "Ulang Tahun · Surabaya", messages: ["8 menit jadi, lagunya bisa custom!!", "Temen-temen pada nanya bikin di mana 😆"], time: "21.03", isSample: true },
  { id: "s-fajar", name: "Fajar & Rara", role: "Pernikahan · Yogyakarta", messages: ["Custom domain-nya bikin undangan terasa eksklusif ✨"], time: "14.50", isSample: true },
  { id: "s-raka", name: "Bu Ratna", role: "Khitan · Solo", messages: ["Tamu tinggal klik link, lokasi langsung kebuka di Maps. Praktis banget."], time: "16.08", isSample: true },
];

const faqs = [
  ["Apakah bisa mencoba gratis?", "Bisa. Kamu dapat membuat dan melihat pratinjau undangan tanpa biaya. Pembayaran hanya diperlukan saat undangan siap dibagikan ke tamu."],
  ["Apakah ada batas jumlah tamu?", "Setiap paket punya kapasitas tamu yang berbeda. Lihat detailnya di bagian harga sebelum memilih paket."],
  ["Berapa lama proses pembuatannya?", "Rata-rata sekitar 10 menit: pilih tema, isi data acara, lalu bagikan link ke tamu."],
  ["Apa maksud masa aktif undangan?", "Masa aktif adalah lama link undanganmu bisa dibuka tamu. Setelah lewat, kamu tetap bisa memperpanjang dari dashboard."],
  ["Apakah tema bisa di-custom?", "Bisa. Ubah foto, warna, teks, musik, dan urutan bagian undangan, lalu lihat pratinjaunya seketika."],
  ["Apakah tersedia program reseller?", "Ya. Vendor WO dan EO bisa menghubungi tim kami lewat WhatsApp untuk informasi program reseller."],
];

async function getJSON<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${path}`, { next: { revalidate: 60 } });
    if (!response.ok) return fallback;
    return response.json();
  } catch {
    return fallback;
  }
}

function shortPrice(amount: number) {
  if (amount <= 0) return { value: "Gratis", unit: "" };
  if (amount % 1000 === 0) return { value: `${(amount / 1000).toLocaleString("id-ID")}rb`, unit: "Rp" };
  return { value: amount.toLocaleString("id-ID"), unit: "Rp" };
}

function planPerks(plan: Plan) {
  const perks = [`Hingga ${plan.max_guests.toLocaleString("id-ID")} tamu`, "RSVP & buku ucapan", "Kirim via WhatsApp"];
  perks.push(plan.has_watermark ? "Dengan watermark Rawuh" : "Tanpa watermark");
  if (plan.custom_domain_allowed) perks.push("Domain pribadi .id");
  if (plan.payment_gateway_allowed) perks.push("Amplop digital");
  perks.push(plan.duration_days ? `Aktif ${plan.duration_days} hari` : "Gratis selamanya untuk 1 undangan");
  return perks;
}

function EventSignup({ label = "Buat gratis" }: { label?: string }) {
  const id = `event-${label.toLowerCase().replace(/\s+/g, "-")}`;
  return (
    <form className={styles.signup} action="/auth/register" method="get">
      <label htmlFor={id} className="sr-only">Nama acaramu</label>
      <input id={id} name="event" placeholder="Nama acaramu, mis. Rina & Bima" autoComplete="off" />
      <button type="submit" className={styles.btnPrimary}>{label}</button>
    </form>
  );
}

export default async function Home() {
  const [hero, kontak, footer, featuresResult, testimonialsResult, templatesResult, plansResult] = await Promise.all([
    getJSON<Hero>("/api/public/site-content/hero", {}),
    getJSON<Kontak>("/api/public/site-content/kontak", {}),
    getJSON<Footer>("/api/public/site-content/footer", {}),
    getJSON<{ items?: Feature[] }>("/api/public/features", {}),
    getJSON<{ items?: Testimonial[] }>("/api/public/testimonials", {}),
    getJSON<{ items?: Template[] }>("/api/templates", {}),
    getJSON<{ items?: Plan[] }>("/api/public/plans", {}),
  ]);

  const extraFeatures = featuresResult.items ?? [];
  const realVoices: Voice[] = (testimonialsResult.items ?? []).map(item => ({
    id: item.id, name: item.name, role: item.role, messages: [item.quote], isSample: item.is_sample,
  }));
  const voices = [...realVoices, ...sampleVoices.slice(0, Math.max(0, 6 - realVoices.length))];
  const templates = templatesResult.items?.length ? templatesResult.items : defaultTemplates;
  const plans = (plansResult.items?.length ? plansResult.items : defaultPlans).slice().sort((a, b) => a.price - b.price);
  const featuredIndex = plans.length >= 3 ? 1 : plans.length - 1;
  const waLink = kontak.whatsapp ? `https://wa.me/${kontak.whatsapp.replace(/[^0-9]/g, "")}` : undefined;
  const heroCta = hero.cta_href && hero.cta_label;

  return (
    <main className={styles.page}>
      <AosInit />
      <a className={styles.skip} href="#konten">Lewati navigasi</a>
      <AnnouncementBar />
      <SiteHeader />

      <div className={styles.rail} id="konten">
        {/* Hero */}
        <section className={styles.hero} aria-labelledby="hero-title">
          <Link href="/#fitur" className={styles.pill}><b>BARU</b> Undangan Video 3D sudah hadir <IconArrowRight size={14} /></Link>
          <h1 id="hero-title" className={styles.heroTitle}>
            {hero.heading ? <span>{hero.heading}</span> : <><span>Undangan yang</span><span>terasa personal.</span></>}
          </h1>
          <p className={styles.lead}>{hero.subheading ?? "Buat undangan website dalam 10 menit dari HP. Kirim ke ratusan tamu, masing-masing dengan namanya."}</p>
          {heroCta ? <a href={hero.cta_href} className={styles.btnPrimary}>{hero.cta_label}</a> : <EventSignup />}
          <div className={styles.proof}>
            <div className={styles.avatars} aria-hidden>
              {[["D", "#E65532"], ["R", "#9CAF88"], ["N", "#C9A66B"], ["F", "#322F2D"]].map(([letter, color]) => <span key={letter} style={{ background: color }}>{letter}</span>)}
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
          {[
            ["120rb+", "undangan dibuat oleh pasangan dan keluarga di seluruh Indonesia."],
            ["500+", "tema siap pakai untuk pernikahan, khitan, aqiqah, hingga ulang tahun."],
            ["10 mnt", "rata-rata waktu dari pilih tema sampai undangan siap dikirim."],
            ["4.9/5", "rating dari 18.000+ ulasan pengguna di Google Play."],
          ].map(([value, label], index) => (
            <div key={value} className={styles.stat} data-aos="fade-up" data-aos-delay={index * 60}><strong>{value}</strong><p>{label}</p></div>
          ))}
        </section>

        <div className={styles.banner}><IconLink size={16} /> Semua acaramu, satu link</div>

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
              <article className={`${styles.card} ${styles.cardWide}`} data-aos="fade-up">
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
              <article className={`${styles.card} ${styles.cardDark}`} data-aos="fade-up" data-aos-delay="60">
                <div className={`${styles.cardVisual} ${styles.rsvpCount}`} aria-hidden>
                  <strong>248</strong><span>dari 320 tamu konfirmasi hadir</span>
                  <div className={styles.bar}><i style={{ width: "78%" }} /></div>
                </div>
                <div className={styles.cardCopy}><h3>RSVP real-time</h3><p>Pantau siapa yang hadir, jumlah tamu, dan pesan menu.</p></div>
              </article>
              <article className={styles.card} data-aos="fade-up">
                <div className={styles.cardVisual} aria-hidden><div className={styles.qrBox}><IconQr /></div></div>
                <div className={styles.cardCopy}><h3>QR Check-in</h3><p>Scan di pintu masuk, daftar hadir terisi otomatis.</p></div>
              </article>
              <article className={styles.card} data-aos="fade-up" data-aos-delay="60">
                <div className={styles.cardVisual} aria-hidden>
                  <div className={styles.player}>
                    <span className={styles.play}><IconPause size={16} /></span>
                    <span className={styles.wave}>{[10, 18, 26, 14, 30, 22, 12, 24, 28, 16, 8, 20, 26, 12, 18, 10, 22, 14].map((h, i) => <i key={i} style={{ height: h }} data-on={i < 8 ? "" : undefined} />)}</span>
                  </div>
                </div>
                <div className={styles.cardCopy}><h3>Musik latar</h3><p>Ratusan lagu, atau unggah lagu kalian sendiri.</p></div>
              </article>
              <article className={styles.card} data-aos="fade-up" data-aos-delay="120">
                <div className={styles.cardVisual} aria-hidden><div className={styles.url}><IconLock size={14} /><b>rinadanbima</b><span>.id</span></div></div>
                <div className={styles.cardCopy}><h3>Domain pribadi</h3><p>Alamat undangan atas nama kalian sendiri.</p></div>
              </article>
              {extraFeatures.map((feature, index) => (
                <article key={feature.id} className={styles.card} style={{ minHeight: 0 }} data-aos="fade-up" data-aos-delay={Math.min(index * 60, 180)}>
                  {feature.icon && <div className={styles.cardVisual} aria-hidden><span className={styles.play}>{feature.icon}</span></div>}
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
            preview: template.preview_image || templateImages[template.slug],
            demoHref: template.preview_url || `/invitation/demo?template=${encodeURIComponent(template.id)}`,
            isPremium: template.is_premium,
          }))} />
        </section>

        {/* How it works */}
        <section className={`${styles.section} ${styles.surface}`} id="cara-kerja" aria-labelledby="steps-title">
          <div className={styles.steps}>
            <div className={styles.titleGroup}>
              <p className={styles.eyebrow}>Cara kerja</p>
              <h2 id="steps-title" className={styles.sectionTitle}>Siap kirim dalam tiga langkah.</h2>
              <p className={styles.lead}>Tidak perlu desainer, tidak perlu laptop. Semua bisa dari HP sambil menunggu fitting baju.</p>
              <Link href="/auth/register" className={styles.btnPrimary}>Mulai buat undangan <IconArrowRight size={14} /></Link>
            </div>
            <ol className={styles.stepList}>
              {[
                ["Pilih tema", "Jelajahi tema, lihat demo langsung, lalu pilih yang paling kamu banget."],
                ["Isi data acara", "Masukkan nama, tanggal, lokasi, foto, dan cerita kalian. Pratinjau berubah seketika."],
                ["Kirim & pantau", "Bagikan ke tamu lewat WhatsApp dan pantau RSVP serta ucapan secara real-time."],
              ].map(([title, desc], index) => (
                <li key={title} data-aos="fade-up" data-aos-delay={index * 60}><b>{String(index + 1).padStart(2, "0")}</b><div><h3>{title}</h3><p>{desc}</p></div></li>
              ))}
            </ol>
          </div>
        </section>

        {/* Pricing */}
        <section className={styles.section} id="harga" aria-labelledby="harga-title">
          <div className={styles.pricing}>
            <div className={styles.titleGroup}>
              <p className={styles.eyebrow}>Harga</p>
              <h2 id="harga-title" className={styles.pricingTitle}><span>Sekali bayar, </span><span>tanpa langganan.</span></h2>
              <p className={styles.pricingDesc}>Hemat hingga 90% dibanding undangan cetak. Bayar hanya saat undangan siap dikirim.</p>
            </div>
            <div className={styles.plans} style={{ "--plans": plans.length } as CSSProperties}>
              {plans.map((plan, index) => {
                const featured = index === featuredIndex && plans.length > 1;
                const price = shortPrice(plan.price);
                const href = plan.price > 0 ? `/auth/login?plan=${encodeURIComponent(plan.id)}` : "/auth/register";
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
                      <Link href={href} className={featured ? styles.btnPrimary : styles.btnOutline}>{plan.price > 0 ? `Pilih ${plan.name}` : "Mulai gratis"}</Link>
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
              <a href={waLink ?? "#faq"} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}>Vendor WO? Program reseller <IconArrowRight size={14} /></a>
            </div>
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
          <a href={waLink ?? "#faq"} className={`${styles.btnOutline} ${styles.voicesMore}`} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}>Ceritakan pengalamanmu</a>
        </section>

        {/* FAQ */}
        <section className={styles.section} id="faq" aria-labelledby="faq-title">
          <div className={styles.faq}>
            <div className={styles.titleGroup}>
              <p className={styles.eyebrow}>FAQ</p>
              <h2 id="faq-title" className={styles.sectionTitle}>Pertanyaan yang sering muncul.</h2>
              <p className={styles.lead}>Masih ragu? Tim kami siap bantu lewat WhatsApp setiap hari, 08.00–22.00.</p>
              <a href={waLink ?? "#kontak"} className={styles.btnOutline} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}>Chat tim support <IconArrowRight size={14} /></a>
            </div>
            <div className={styles.faqList}>
              {faqs.map(([question, answer], index) => (
                <details key={question} open={index === 0}>
                  <summary>{question}<span className={styles.faqToggle} aria-hidden><IconPlus className={styles.plus} size={16} /><IconMinus className={styles.minus} size={16} /></span></summary>
                  <p>{answer}</p>
                </details>
              ))}
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className={`${styles.section} ${styles.surface} ${styles.cta}`} id="kontak" aria-labelledby="cta-title">
          <div className={styles.titleGroup}>
            <p className={styles.eyebrow}>Mulai sekarang</p>
            <h2 id="cta-title" className={styles.ctaTitle}>
              {kontak.heading ? <span style={{ color: "var(--rw-ink)" }}>{kontak.heading}</span> : <><span>Tamu menunggu kabar bahagiamu.</span><span>Kirim undangannya hari ini.</span></>}
            </h2>
            {kontak.subheading && <p className={styles.lead}>{kontak.subheading}</p>}
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
      </div>

      <SiteFooter copyright={footer.copyright} instagram={footer.instagram} whatsappHref={waLink} />
    </main>
  );
}
