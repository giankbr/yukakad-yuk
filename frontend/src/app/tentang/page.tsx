import type { Metadata } from "next";
import Image from "next/image";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, FinalCta, MarketingPage, SplitTitle } from "@/components/landing/Sections";
import { IconHandshake, IconMail, IconPin, IconWhatsapp } from "@/components/brand/icons";
import { getAbout, getSiteContact } from "@/lib/marketing";
import { isRemoteImage } from "@/lib/site-content";

export const metadata: Metadata = {
  title: "Tentang Kami | Rawuh",
  description: "Rawuh artinya “datang”. Kenali cerita, prinsip, dan tim di balik undangan digital Rawuh dari Yogyakarta.",
};

export default async function TentangPage() {
  const [{ kontak, waLink }, about] = await Promise.all([getSiteContact(), getAbout()]);
  const whatsappLabel = kontak.whatsapp ?? "+62 811 2600 2100";
  return (
    <MarketingPage current="tentang">
      <section className={styles.head} style={{ borderBottom: 0, paddingBottom: 40 }} aria-labelledby="about-title">
        <Breadcrumb items={[["Beranda", "/"], ["Tentang kami"]]} />
        <div className={styles.aboutHead}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Tentang Rawuh</p>
            <SplitTitle as="h1" id="about-title" className={styles.h1} lead={about.title_lead} mono={about.title_mono} />
          </div>
          <p className={styles.lead}>{about.lead}</p>
        </div>
      </section>
      <div className={styles.heroPhoto}>
        <Image src={about.photo} unoptimized={isRemoteImage(about.photo)} alt="Tim Rawuh" fill sizes="(max-width: 1280px) 100vw, 1120px" preload />
      </div>
      <div className={styles.statRow}>
        {about.stats.map(({ value, label }) => (
          <div key={label}><strong>{value}</strong><small>{label}</small></div>
        ))}
      </div>

      <section className={base.section} aria-labelledby="story-title">
        <div className={styles.story}>
          <div className={base.titleGroup} style={{ alignContent: "start" }}>
            <p className={base.eyebrow}>Cerita kami</p>
            <h2 id="story-title" className={base.sectionTitle}>{about.story_title}</h2>
          </div>
          <div className={styles.storyBody}>
            {about.story.split(/\n\s*\n/).filter(p => p.trim()).map((paragraph, i) => <p key={i}>{paragraph.trim()}</p>)}
            {about.quote.trim() && (
              <blockquote className={styles.quote}>
                <p>{about.quote}</p>
                {about.quote_by.trim() && <cite>— {about.quote_by}</cite>}
              </blockquote>
            )}
          </div>
        </div>
      </section>

      <section className={base.section} aria-labelledby="principles-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Yang kami pegang</p>
          <SplitTitle id="principles-title" className={base.splitInline} lead={about.principles.length === 4 ? "Empat prinsip," : "Prinsip kami,"} mono="setiap hari." />
        </div>
        <div className={styles.principles}>
          {about.principles.map(({ title, text: desc }, index) => <div key={title}><b>{String(index + 1).padStart(2, "0")}</b><h3>{title}</h3><p>{desc}</p></div>)}
        </div>
      </section>

      <section className={base.section} aria-labelledby="journey-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Perjalanan</p>
          <h2 id="journey-title" className={base.sectionTitle}>{about.journey_title}</h2>
        </div>
        <ol className={styles.timeline}>
          {about.milestones.map(({ year, title, text: desc }) => <li key={`${year}-${title}`}><i aria-hidden /><strong>{year}</strong><h3>{title}</h3><p>{desc}</p></li>)}
        </ol>
      </section>

      <section className={base.section} id="tim" style={{ borderBottom: 0 }} aria-labelledby="team-title">
        <div className={styles.headRow} style={{ marginBottom: 40 }}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Tim</p>
            <h2 id="team-title" className={base.sectionTitle}>{about.team_title}</h2>
          </div>
          {about.open_roles.trim() && <a className={styles.openRoles} href={waLink ?? `mailto:${about.email}`} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}><i aria-hidden />{about.open_roles}</a>}
        </div>
        <div className={styles.team}>
          {about.team.map(({ name, role, photo }) => (
            <figure key={name}>
              <div>{photo ? <Image src={photo} unoptimized={isRemoteImage(photo)} alt={`Foto ${name}`} fill sizes="(max-width: 560px) 50vw, 25vw" /> : <span aria-hidden style={{ display: "grid", placeItems: "center", height: "100%", color: "var(--rw-primary)", fontSize: 40, fontWeight: 600 }}>{name.split(/\s+/).slice(0, 2).map(w => w[0]).join("").toUpperCase()}</span>}</div>
              <strong>{name}</strong>
              <small>{role}</small>
            </figure>
          ))}
        </div>
      </section>

      <div className={styles.contacts} id="kontak">
        <div><IconPin size={16} /><small>Kantor</small><p>{about.address}</p></div>
        <div><IconMail size={16} /><small>Email</small><a href={`mailto:${about.email}`}>{about.email}</a></div>
        <div><IconWhatsapp size={16} /><small>WhatsApp</small>{waLink ? <a href={waLink} target="_blank" rel="noreferrer">{whatsappLabel}</a> : <p>{whatsappLabel}</p>}</div>
        <div><IconHandshake size={16} /><small>Kemitraan</small><a href="/reseller">Reseller &amp; Wedding Organizer</a></div>
      </div>

      <FinalCta />
    </MarketingPage>
  );
}
