"use client";
/* eslint-disable @next/next/no-img-element -- Invitation photos can use user-supplied URLs. */
// Layout recreated in React/CSS after https://weddings-one-page-template.webflow.io/ (no Webflow source or assets).
import Link from "next/link";
import { useRef, useState } from "react";
import { CopyButton } from "@/components/ui/CopyButton";
import { sendRSVP } from "./RSVPSection";
import type { InvitationData } from "./types";
import styles from "./WeddingsOnePage.module.css";

const icon = { width: 16, height: 16, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.5, "aria-hidden": true } as const;
const Clock = () => <svg {...icon}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></svg>;
const Pin = () => <svg {...icon}><path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12Z" /><circle cx="12" cy="9" r="2.5" /></svg>;
const Spark = () => <svg {...icon}><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6" /></svg>;

// Scroll reveal attributes, animated by AosInit (disabled for reduced motion).
const aos = (effect = "fade-up", delay = 0) => ({ "data-aos": effect, "data-aos-delay": delay });

function Photo({ src, alt, eager = false }: { src?: string; alt: string; eager?: boolean }) {
  return src ? <img className={styles.image} src={src} alt={alt} loading={eager ? "eager" : "lazy"} /> : <div className={styles.image} role="img" aria-label={alt} />;
}

function format(value: string, options: Intl.DateTimeFormatOptions) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat("id-ID", { ...options, timeZone: "Asia/Jakarta" }).format(date);
}

function Button({ href, children }: { href: string; children: string }) {
  return <a className={styles.button} href={href}><span>{children}</span><span className={styles.buttonHover} aria-hidden>{children}</span></a>;
}

function Slider({ images, alt }: { images: string[]; alt: string }) {
  const track = useRef<HTMLDivElement>(null);
  const move = (direction: number) => track.current?.scrollBy({ left: direction * track.current.clientWidth * 0.6, behavior: "smooth" });
  const captions = ["Awal dari semuanya", "Hari-hari sederhana", "Tawa yang kami simpan", "Menuju selamanya"];
  return <div className={styles.slider}>
    <div ref={track} className={styles.sliderTrack} tabIndex={0} aria-label="Galeri foto">
      {images.map((src, index) => <figure key={`${src}-${index}`} className={styles.slide} {...aos("fade-left", Math.min(index, 3) * 90)}>
        <div className={styles.media}><Photo src={src} alt={`${alt}, foto ${index + 1}`} /></div><figcaption className={styles.label}>{captions[index % captions.length]}</figcaption>
      </figure>)}
    </div>
    {images.length > 1 && <div className={styles.sliderArrows} {...aos("fade-up", 120)}>
      <button type="button" onClick={() => move(-1)} aria-label="Foto sebelumnya">←</button>
      <button type="button" onClick={() => move(1)} aria-label="Foto berikutnya">→</button>
    </div>}
  </div>;
}

function RSVPForm({ slug, guestToken, guestName, demo }: { slug: string; guestToken?: string; guestName?: string; demo: boolean }) {
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  if (sent) return <p className={styles.state} role="status">{demo ? "Preview berhasil. Jawaban contoh tidak dikirim." : "Terima kasih! Jawabanmu sudah kami terima."}</p>;
  return <form className={styles.form} {...aos("fade-up", 100)} onSubmit={async (event) => {
    event.preventDefault();
    if (pending) return;
    setError("");
    if (demo) { setSent(true); return; }
    const form = new FormData(event.currentTarget);
    const guests = Math.min(10, Math.max(1, Number(form.get("guests")) || 1));
    setPending(true);
    try {
      await sendRSVP(slug, { guest_token: guestToken, attendance: form.get("attendance"), attendees_count: guests, message: `${form.get("name")}: ${form.get("message") ?? ""}` });
      setSent(true);
    } catch { setError("Jawaban belum tersimpan. Periksa koneksi lalu coba lagi."); }
    finally { setPending(false); }
  }}>
    <div className={styles.formGrid}>
      <label className={styles.formRow}><span className={styles.formLabel}>Nama lengkap *</span><input className={styles.field} required name="name" maxLength={100} autoComplete="name" defaultValue={guestName} placeholder="Nama kamu" /></label>
      <label className={styles.formRow}><span className={styles.formLabel}>Jumlah tamu *</span><input className={styles.field} required name="guests" type="number" min={1} max={10} defaultValue={1} /></label>
      <label className={`${styles.formRow} ${styles.full}`}><span className={styles.formLabel}>Ucapan & doa</span><textarea className={`${styles.field} ${styles.message}`} name="message" maxLength={850} placeholder="Tulis pesan untuk kami (opsional)" /></label>
      <div className={`${styles.formRow} ${styles.full}`} role="radiogroup" aria-label="Kehadiran">
        <label className={styles.radio}><input type="radio" name="attendance" value="yes" defaultChecked /><span className={styles.label}>Saya akan hadir</span></label>
        <label className={styles.radio}><input type="radio" name="attendance" value="no" /><span className={styles.label}>Maaf, saya berhalangan hadir</span></label>
      </div>
    </div>
    <button className={styles.button} type="submit" disabled={pending}>{pending ? "Mengirim…" : "Kirim RSVP"}</button>
    {error && <p className={`${styles.state} ${styles.stateError}`} role="alert">{error}</p>}
  </form>;
}

function Tabs({ data }: { data: InvitationData }) {
  const [active, setActive] = useState(0);
  const tabs = [
    { title: data.story.title, body: data.story.body },
    { title: data.place, body: data.address },
    { title: "Dari kami berdua", body: data.couple.note },
  ].filter((tab) => tab.body);
  const image = (index: number) => data.gallery.length ? data.gallery[(index + 1) % data.gallery.length] : undefined;
  return <div className={styles.tabs}>
    <div className={styles.tabImage} {...aos("fade-right")}><Photo key={active} src={image(active)} alt={tabs[active]?.title ?? "Cerita kami"} /></div>
    <div className={styles.tabMenu} role="tablist" {...aos("fade-left", 120)}>
      {tabs.map((tab, index) => <button key={tab.title} type="button" role="tab" aria-selected={active === index} className={styles.tabLink} onClick={() => setActive(index)}>
        <span className={styles.displayXs}>{tab.title}</span><span className={styles.body}>{tab.body}</span>
      </button>)}
    </div>
  </div>;
}

export function WeddingsOnePage({ data, slug, guestToken, demo = false }: { data: InvitationData; slug: string; guestToken?: string; demo?: boolean }) {
  const { bride, groom } = data.couple;
  const date = format(data.date, { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  const time = format(data.date, { hour: "2-digit", minute: "2-digit" });
  const photos = data.gallery;
  const mapsUrl = data.mapsUrl && /^https?:\/\//i.test(data.mapsUrl) ? data.mapsUrl : undefined;
  const faqs = [
    { q: "Bolehkah membawa tamu tambahan?", a: "Mohon isi jumlah tamu pada form RSVP agar kami bisa menyiapkan tempat untuk semua.", link: { href: "#rsvp", label: "Isi RSVP" } },
    { q: "Di mana acaranya berlangsung?", a: `${data.place}, ${data.address}.`, link: mapsUrl ? { href: mapsUrl, label: "Buka peta" } : undefined },
    { q: "Bagaimana susunan acaranya?", a: data.events.map((event) => `${event.name} pukul ${event.time}`).join(", ") + ".", link: { href: "#timeline", label: "Lihat timeline" } },
    ...(data.gifts.length ? [{ q: "Apakah ada informasi hadiah?", a: "Kehadiranmu sudah lebih dari cukup. Bila ingin mengirim tanda kasih, detailnya ada di bawah.", link: { href: "#gifts", label: "Lihat detail" } }] : []),
  ];

  return <main className={styles.page}>
    {/* eslint-disable-next-line @next/next/no-page-custom-font -- Fonts are scoped to invitation routes (App Router). */}
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&display=swap" />
    {demo && <aside className={styles.preview}>Preview template weddings · Data contoh <Link href="/dashboard/invitations/create">Buat undangan sendiri ↗</Link></aside>}
    <div className={styles.progress} aria-hidden />
    <div className={styles.topBar}><p className={styles.bodyS}>Selamat datang di pernikahan kami pada {date} di {data.place}</p></div>
    <nav className={styles.nav} aria-label="Navigasi undangan">
      <div className={styles.navLinks}><a href="#info">Info</a><a href="#timeline">Timeline</a><a href="#story">Cerita</a><a href="#faq">FAQ</a></div>
      <a href="#home" className={styles.brand} aria-label={`${bride} & ${groom}`}>{bride.slice(0, 1)}&amp;{groom.slice(0, 1)}</a>
      <div className={styles.navRight}><a href="#rsvp">RSVP</a></div>
    </nav>

    <section id="home" className={`${styles.section} ${styles.hero}`}>
      <div className={styles.heroTitle}>
        <div className={styles.line}><p className={`${styles.label} ${styles.reveal}`}>{date}</p></div>
        <h1 className={styles.display2xl}><span className={styles.line}><span className={styles.reveal}>{bride}</span></span><span className={styles.line}><span className={styles.reveal}>&amp; {groom}</span></span></h1>
        {data.guestName && <p className={styles.guest}>Kepada Yth. <strong>{data.guestName}</strong></p>}
        <div className={styles.heroButton}><Button href="#rsvp">RSVP</Button></div>
      </div>
      <div className={styles.heroImages}>
        {[photos[0], photos[1] ?? photos[0]].map((src, index) => <div key={index} className={styles.heroImage}><Photo src={src} alt={`${bride} dan ${groom}`} eager /><div className={styles.overlay} /></div>)}
      </div>
      <div className={styles.heroBackground}><div className={styles.heroSplit} /></div>
    </section>

    <section id="info" className={`${styles.section} ${styles.info}`}>
      <div className={styles.container}>
        <p className={styles.displayL} {...aos()}>Kami dipertemukan di waktu yang tepat, dan kini menghitung hari menuju kata <em>sah</em>.</p>
        <ul className={styles.infoList}>
          <li {...aos("fade-up", 0)}><Clock /><span className={styles.label}>{date}{time !== data.date && ` pukul ${time}`}</span></li>
          <li {...aos("fade-up", 90)}><Pin /><span className={styles.label}>{data.place}, {data.address}</span></li>
          {mapsUrl && <li {...aos("fade-up", 180)}><Spark /><a className={styles.label} href={mapsUrl} target="_blank" rel="noreferrer">Petunjuk lokasi ↗</a></li>}
        </ul>
        {photos.length > 0 && <Slider images={photos} alt={`Kenangan ${bride} dan ${groom}`} />}
      </div>
    </section>

    <section id="timeline" className={styles.section}>
      <div className={`${styles.container} ${styles.stack}`}>
        <div className={styles.title} {...aos()}><p className={styles.label}>Timeline</p><p className={styles.displayL}>Dari akad hingga perpisahan terakhir, inilah rangkaian hari bahagia yang akan kita lalui bersama.</p></div>
        <div className={styles.timetable}>
          {data.events.map((event, index) => <article key={`${event.name}-${index}`} className={styles.timelineItem} {...aos("fade-up", Math.min(index, 4) * 80)}>
            <p className={styles.displayXs}>{event.time}</p>
            <div className={styles.timelineBody}>
              <h3 className={styles.displayXs}>{event.name}</h3>
              <p className={styles.bodyL}>{format(event.date, { weekday: "long", day: "numeric", month: "long", year: "numeric" })}</p>
              <p className={styles.subheader}><Pin /><span className={styles.label}>{event.venue || data.place}</span></p>
            </div>
          </article>)}
        </div>
      </div>
    </section>

    <section id="rsvp" className={`${styles.section} ${styles.rsvp}`}>
      <div className={styles.containerL}><div className={styles.rsvpImage} {...aos("zoom-out")}><Photo src={photos[2] ?? photos[0]} alt={`${bride} dan ${groom}`} /></div></div>
      <div className={`${styles.container} ${styles.rsvpTitle}`} {...aos()}>
        <p className={styles.subheader}><Spark /><span className={styles.label}>RSVP</span></p>
        <h2 className={styles.displayXl}>Kami akan senang sekali jika kamu bisa hadir di hari istimewa kami</h2>
        <p className={styles.body}>Mohon isi form di bawah sebelum {format(data.date, { day: "numeric", month: "long", year: "numeric" })}</p>
      </div>
      <div className={styles.container}><RSVPForm slug={slug} guestToken={guestToken} guestName={data.guestName} demo={demo} /></div>
      <div className={styles.sectionBackground}><div className={styles.sectionSplit} /></div>
    </section>

    <section id="story" className={styles.section}>
      <div className={`${styles.container} ${styles.stack}`}>
        <div className={`${styles.title} ${styles.titleS}`} {...aos()}><p className={styles.label}>Cerita kami</p><p className={styles.displayXl}>Terima kasih sudah menjadi bagian dari perjalanan kami</p></div>
        <Tabs data={data} />
      </div>
    </section>

    {data.gifts.length > 0 && <section id="gifts" className={styles.section}>
      <div className={`${styles.container} ${styles.stack}`}>
        <div className={styles.title} {...aos()}><p className={styles.label}>Tanda kasih</p><p className={styles.displayL}>Doa restumu adalah hadiah terindah. Bila ingin berbagi lebih, berikut caranya.</p></div>
        <div className={styles.gifts}>{data.gifts.map((gift, index) => {
          const [name, value, extra] = gift.type === "bank" ? [gift.bank_name, gift.account_number, gift.account_name && `a.n. ${gift.account_name}`]
            : gift.type === "ewallet" ? [gift.ewallet_provider, gift.ewallet_number, undefined]
            : gift.type === "address" ? ["Alamat kirim hadiah", gift.address, undefined] : ["QRIS", undefined, undefined];
          return <div key={gift.id} className={styles.gift} {...aos("fade-up", Math.min(index, 3) * 90)}>
            <p className={styles.label}>{name}</p>
            {value && <p className={styles.displayS}>{value}</p>}
            {extra && <p className={styles.body}>{extra}</p>}
            {gift.type === "qris" && gift.qris_image_url && <img src={gift.qris_image_url} alt="Kode QRIS" className={styles.qris} />}
            {value && gift.type !== "address" && <CopyButton value={value} />}
          </div>;
        })}</div>
      </div>
    </section>}

    <section id="faq" className={styles.section}>
      <div className={styles.container}>
        <div className={styles.faqHeader} {...aos()}><p className={styles.displayXs}>Tanya & jawab</p></div>
        {faqs.map((faq, index) => <details key={faq.q} className={styles.faqItem} {...aos("fade-up", Math.min(index, 4) * 70)}>
          <summary><span className={styles.displayXs}>({String(index + 1).padStart(2, "0")})</span><span className={styles.displayXs}>{faq.q}</span><span className={styles.faqIcon} aria-hidden>+</span></summary>
          <div className={styles.faqBody}><p className={styles.bodyL}>{faq.a}</p>{faq.link && <a className={styles.link} href={faq.link.href} {...(faq.link.href.startsWith("http") ? { target: "_blank", rel: "noreferrer" } : {})}>{faq.link.label}</a>}</div>
        </details>)}
        <div className={styles.faqLast} {...aos()}><p className={`${styles.displayM} ${styles.light}`}>Masih ada pertanyaan?</p><a className={styles.displayM} href="#rsvp">Tulis di pesan RSVP</a></div>
      </div>
    </section>

    <footer className={`${styles.section} ${styles.footer}`}>
      <div className={`${styles.container} ${styles.footerGrid}`} {...aos()}>
        <div className={styles.footerItem}><span className={styles.footerBrand}>{bride.slice(0, 1)}&amp;{groom.slice(0, 1)}</span><p className={styles.body}>{data.couple.note}</p><p className={styles.body}>Dibuat dengan cinta · <Link className={styles.link} href="/">Yukakad</Link></p></div>
        <div className={styles.footerMenu}><p className={styles.label}>Undangan</p><a href="#info">Info</a><a href="#timeline">Timeline</a><a href="#rsvp">RSVP</a><a href="#story">Cerita</a><a href="#faq">FAQ</a></div>
        <div className={styles.footerMenu}><p className={styles.label}>Hari bahagia</p><span>{date}</span><span>{data.place}</span><a href="#home">Kembali ke atas ↑</a></div>
      </div>
      <div className={`${styles.sectionBackground} ${styles.footerBackground}`} />
    </footer>
  </main>;
}
