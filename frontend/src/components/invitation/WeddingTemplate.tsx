/* eslint-disable @next/next/no-img-element -- Invitation photos can use user-supplied URLs. */
import type { InvitationData } from "./types";
import Link from "next/link";
import { CountdownSection } from "./CountdownSection";
import { GiftSection } from "./GiftSection";
import { RSVPSection } from "./RSVPSection";
import styles from "./WeddingTemplate.module.css";
import { WeddingsOnePage } from "./WeddingsOnePage";
import { AosInit } from "@/components/landing/AosInit";

export const weddingTemplates = ["alyra", "weddings", "veloria"] as const;
export type WeddingStyle = typeof weddingTemplates[number];
export function isWeddingStyle(value?: string): value is WeddingStyle {
  return weddingTemplates.some((template) => template === value);
}

// Scroll reveal attributes, animated by AosInit (disabled for reduced motion).
const aos = (effect = "fade-up", delay = 0) => ({ "data-aos": effect, "data-aos-delay": delay });

function Photo({ src, alt, eager = false }: { src?: string; alt: string; eager?: boolean }) {
  return src ? <img src={src} alt={alt} loading={eager ? "eager" : "lazy"} /> : <div className={styles.emptyPhoto} aria-label="Dekorasi undangan"><span>With love</span></div>;
}

function dateLabel(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat("id-ID", { dateStyle: "long", timeZone: "Asia/Jakarta" }).format(date);
}

export function WeddingTemplate({ variant, data, slug, guestToken, demo = false }: {
  variant: WeddingStyle; data: InvitationData; slug: string; guestToken?: string; demo?: boolean;
}) {
  if (variant === "weddings") return <><AosInit /><WeddingsOnePage data={data} slug={slug} guestToken={guestToken} demo={demo} /></>;
  const { bride, groom } = data.couple;
  const initials = `${bride.slice(0, 1)} & ${groom.slice(0, 1)}`;
  const date = dateLabel(data.date);
  return <main className={`${styles.page} ${styles[variant]}`}>
    <AosInit />
    {/* Fonts are intentionally scoped to invitation routes (App Router). */}
    {/* eslint-disable-next-line @next/next/no-page-custom-font */}
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gilda+Display&family=Newsreader:ital,wght@0,400;1,400&family=Carattere&display=swap" />
    {demo && <aside className={styles.preview}>Preview template {variant} · Data contoh <Link href="/dashboard/invitations/create">Buat undangan sendiri ↗</Link></aside>}
    {variant === "veloria" && <div className={styles.veloriaRail}><span>Wedding day · {date}</span><span>Celebrate love</span><span>{data.place}</span></div>}
    <nav className={styles.nav} aria-label="Navigasi undangan">
      <a href="#home" className={styles.monogram}>{initials}</a>
      <div><a href="#story">Cerita kami</a><a href="#day">Hari bahagia</a><a href="#memories">Galeri</a></div>
      <a href="#rsvp" className={styles.navRsvp}>RSVP ↗</a>
    </nav>
    <header id="home" className={styles.hero}>
      {variant === "alyra" ? <>
        <p className={styles.eyebrow}>The wedding of</p>
        <div className={styles.alyraNames}><h1><span>{bride} &</span><span>{groom}</span></h1><div className={styles.alyraPhoto}><Photo src={data.gallery[0]} alt={`${bride} dan ${groom}`} eager /></div></div>
        <div className={styles.heroBottom}><p>{date}<br />{data.place}</p><p>Satu cerita. Seumur hidup.<br /><a href="#story">Kenali cerita kami ↗</a></p><a className={styles.circle} href="#rsvp">RSVP<br />↗</a></div>
      </> : <>
        <div className={styles.veloriaHero}>
          <div className={styles.veloriaStack}>
            <figure className={styles.veloriaMainPhoto}><Photo src={data.gallery[0]} alt={`Pernikahan ${bride} dan ${groom}`} eager /></figure>
            <figure className={styles.veloriaFloatTop}><Photo src={data.gallery[1] ?? data.gallery[0]} alt="" eager /></figure>
            <figure className={styles.veloriaFloatRing}><Photo src={data.gallery[2] ?? data.gallery[0]} alt="" /></figure>
          </div>
          <div className={styles.veloriaCopy}>
            <p className={styles.eyebrow}>Celebrate love, stress-free</p>
            <h1>{bride}<em>&</em>{groom}</h1>
            <p className={styles.veloriaLead}>Crafting a beautiful wedding day with passion &amp; precision — kami mengundangmu menjadi bagian dari cerita ini.</p>
            <div className={styles.veloriaCtas}>
              <a className={styles.button} href="#rsvp">Rayakan bersama kami <span>→</span></a>
              <a className={styles.veloriaGhost} href="#day">Lihat rangkaian acara</a>
            </div>
            <div className={styles.veloriaStats}>
              <div><strong>01</strong><span>{date}</span></div>
              <div><strong>02</strong><span>{data.place}</span></div>
              <div><strong>03</strong><span>RSVP terbuka</span></div>
            </div>
          </div>
        </div>
      </>}
    </header>
    {data.guestName && <div className={styles.guest}>Dengan penuh cinta, kami mengundang <strong>{data.guestName}</strong></div>}
    <section id="story" className={styles.story}>
      <div {...aos("fade-right")}><p className={styles.eyebrow}>01 / Our story</p><h2>{data.story.title}</h2><p>{data.story.body}</p><p className={styles.script}>{bride} & {groom}</p></div>
      <figure {...aos("fade-left", 120)}><Photo src={data.gallery[1] ?? data.gallery[0]} alt="Kenangan perjalanan kami" /><figcaption>Little moments, a lifetime of memories.</figcaption></figure>
    </section>
    <div className={styles.countdown} {...aos()}><CountdownSection data={data} /></div>
    <section id="day" className={styles.day}>
      <div className={styles.sectionHeading} {...aos()}><p className={styles.eyebrow}>02 / The wedding day</p><h2>Hari yang kami nantikan.<br /><em>Bersama kalian.</em></h2><p>{date} · {data.place}</p></div>
      <div className={styles.events}>{data.events.map((event, index) => <article key={`${event.name}-${index}`} {...aos("fade-up", Math.min(index, 4) * 90)}><span className={styles.eyebrow}>0{index + 1}</span><h3>{event.name}</h3><p>{dateLabel(event.date)}</p><p>{event.time}</p><p>{event.venue}</p></article>)}</div>
      <div className={styles.location} {...aos()}><div><p className={styles.eyebrow}>Meet us here</p><h3>{data.place}</h3><p>{data.address}</p></div>{data.mapsUrl && /^https?:\/\//i.test(data.mapsUrl) && <a className={styles.button} href={data.mapsUrl} target="_blank" rel="noreferrer">Petunjuk lokasi ↗</a>}</div>
    </section>
    {data.gallery.length > 0 && <section id="memories" className={styles.memories}><div className={styles.sectionHeading} {...aos()}><p className={styles.eyebrow}>03 / In good company</p><h2>Momen kecil,<br /><em>kenangan selamanya.</em></h2></div><div className={styles.gallery}>{data.gallery.map((src, index) => <figure key={`${src}-${index}`} {...aos("fade-up", (index % 3) * 90)}><Photo src={src} alt={`Kenangan ${bride} dan ${groom}, foto ${index + 1}`} /><figcaption>({String(index + 1).padStart(2, "0")}) A moment to keep</figcaption></figure>)}</div></section>}
    <div id="rsvp" className={styles.response} {...aos()}><RSVPSection slug={slug} guestToken={guestToken} demo={demo} /></div>
    <div className={styles.gifts} {...aos()}><GiftSection data={data} /></div>
    <footer className={styles.footer} {...aos("fade-in")}><p className={styles.eyebrow}>The beginning of forever</p><h2>{bride} <em>&</em> {groom}</h2><p>Terima kasih sudah menjadi bagian dari cerita kami.</p><div><span>{date}</span><a href="#home">Kembali ke atas ↑</a><Link href="/">Made with love · Yukakad</Link></div></footer>
  </main>;
}
