import type { Metadata } from "next";
import Image from "next/image";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, FinalCta, MarketingPage, SplitTitle } from "@/components/landing/Sections";
import { IconHandshake, IconMail, IconMessage, IconPin } from "@/components/brand/icons";
import { getSiteContact } from "@/lib/marketing";

export const metadata: Metadata = {
  title: "Tentang Kami | Rawuh",
  description: "Rawuh artinya “datang”. Kenali cerita, prinsip, dan tim di balik undangan digital Rawuh dari Yogyakarta.",
};

const principles = [
  ["Personal, bukan massal", "Setiap tamu pantas disapa dengan namanya."],
  ["Ramah untuk orang tua", "Kalau ibu kami bisa pakai, semua orang bisa."],
  ["Harga jujur", "Sekali bayar. Tanpa langganan, tanpa jebakan."],
  ["Lokal sepenuhnya", "Desainer, server, dan CS ada di Indonesia."],
];

const milestones = [
  ["2021", "Undangan pertama", "Dibuat untuk pernikahan kakak, 50 tamu."],
  ["2022", "Rawuh.id lahir", "10 tema pertama & fitur RSVP."],
  ["2023", "Amplop digital", "QRIS & e-wallet, 10rb acara."],
  ["2024", "QR Check-in", "Buku tamu tanpa antre di venue."],
  ["2026", "Video 3D", "120rb+ acara di 34 provinsi."],
];

const team = [
  ["Galih Prakoso", "Pendiri & CEO", "/rawuh/team-galih.webp"],
  ["Sekar Ayuningtyas", "Kepala Desain", "/rawuh/team-sekar.webp"],
  ["Bagus Wicaksono", "Kepala Teknologi", "/rawuh/team-bagus.webp"],
  ["Nadia Putri", "Customer Happiness", "/rawuh/team-nadia.webp"],
];

export default async function TentangPage() {
  const { kontak, waLink } = await getSiteContact();
  const whatsappLabel = kontak.whatsapp ?? "+62 811 2600 2100";
  return (
    <MarketingPage current="tentang">
      <section className={styles.head} style={{ borderBottom: 0, paddingBottom: 40 }} aria-labelledby="about-title">
        <Breadcrumb items={[["Beranda", "/"], ["Tentang kami"]]} />
        <div className={styles.aboutHead}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Tentang Rawuh</p>
            <SplitTitle as="h1" id="about-title" className={styles.h1} lead="Rawuh artinya" mono="“datang.”" />
          </div>
          <p className={styles.lead}>Dalam bahasa Jawa, rawuh adalah cara paling sopan untuk menyebut kedatangan seseorang. Kami membangun Rawuh agar setiap tamu merasa diundang secara pribadi — bukan sekadar menerima link.</p>
        </div>
      </section>
      <div className={styles.heroPhoto}>
        <Image src="/rawuh/about-team.webp" alt="Tim Rawuh berdiskusi di kantor Yogyakarta" fill sizes="(max-width: 1280px) 100vw, 1120px" preload />
      </div>
      <div className={styles.statRow}>
        {[["2021", "berdiri di Yogyakarta"], ["120rb+", "acara dirayakan"], ["2,4 jt", "tamu diundang"], ["34", "provinsi terjangkau"]].map(([value, label]) => (
          <div key={label}><strong>{value}</strong><small>{label}</small></div>
        ))}
      </div>

      <section className={base.section} aria-labelledby="story-title">
        <div className={styles.story}>
          <div className={base.titleGroup} style={{ alignContent: "start" }}>
            <p className={base.eyebrow}>Cerita kami</p>
            <h2 id="story-title" className={base.sectionTitle}>Berawal dari undangan nikah kakak kami sendiri.</h2>
          </div>
          <div className={styles.storyBody}>
            <p>Tahun 2021, pernikahan dibatasi 50 tamu. Kakak kami ingin keluarga di Medan, Makassar, dan Belanda tetap merasa hadir. Undangan digital yang ada saat itu terasa dingin — satu link yang sama untuk semua orang.</p>
            <p>Jadi kami membuatnya sendiri: undangan dengan nama setiap tamu, peta yang benar-benar bisa dipakai, dan buku ucapan yang dibaca ulang bertahun-tahun kemudian. Teman-teman mulai minta dibuatkan. Lalu teman dari teman.</p>
            <blockquote className={styles.quote}>
              <p>Teknologi boleh modern, tapi rasa diundangnya harus tetap seperti diantar langsung ke rumah.</p>
              <cite>— Galih Prakoso, pendiri</cite>
            </blockquote>
          </div>
        </div>
      </section>

      <section className={base.section} style={{ background: "var(--rw-surface-2)" }} aria-labelledby="principles-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Yang kami pegang</p>
          <SplitTitle id="principles-title" className={base.splitInline} lead="Empat prinsip," mono="setiap hari." />
        </div>
        <div className={styles.principles}>
          {principles.map(([title, desc], index) => <div key={title}><b>{String(index + 1).padStart(2, "0")}</b><h3>{title}</h3><p>{desc}</p></div>)}
        </div>
      </section>

      <section className={base.section} aria-labelledby="journey-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Perjalanan</p>
          <h2 id="journey-title" className={base.sectionTitle}>Dari satu undangan ke 120 ribu.</h2>
        </div>
        <ol className={styles.timeline}>
          {milestones.map(([year, title, desc]) => <li key={year}><i aria-hidden /><strong>{year}</strong><h3>{title}</h3><p>{desc}</p></li>)}
        </ol>
      </section>

      <section className={base.section} id="tim" style={{ borderBottom: 0 }} aria-labelledby="team-title">
        <div className={styles.headRow} style={{ marginBottom: 40 }}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Tim</p>
            <h2 id="team-title" className={base.sectionTitle}>24 orang, satu kantor di Jogja.</h2>
          </div>
          <a className={styles.openRoles} href={waLink ?? "mailto:halo@rawuh.id"} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}><i aria-hidden />3 posisi terbuka — hubungi kami</a>
        </div>
        <div className={styles.team}>
          {team.map(([name, role, photo]) => (
            <figure key={name}>
              <div><Image src={photo} alt={`Foto ${name}`} fill sizes="(max-width: 560px) 50vw, 25vw" /></div>
              <strong>{name}</strong>
              <small>{role}</small>
            </figure>
          ))}
        </div>
      </section>

      <div className={styles.contacts} id="kontak">
        <div><IconPin size={16} /><small>Kantor</small><p>Jl. Prawirotaman No. 12, Yogyakarta</p></div>
        <div><IconMail size={16} /><small>Email</small><a href="mailto:halo@rawuh.id">halo@rawuh.id</a></div>
        <div><IconMessage size={16} /><small>WhatsApp</small>{waLink ? <a href={waLink} target="_blank" rel="noreferrer">{whatsappLabel}</a> : <p>{whatsappLabel}</p>}</div>
        <div><IconHandshake size={16} /><small>Kemitraan</small>{waLink ? <a href={waLink} target="_blank" rel="noreferrer">Reseller &amp; Wedding Organizer</a> : <p>Reseller &amp; Wedding Organizer</p>}</div>
      </div>

      <FinalCta />
    </MarketingPage>
  );
}
