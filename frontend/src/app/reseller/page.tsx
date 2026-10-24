import type { Metadata } from "next";
import Link from "next/link";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, FaqSection, MarketingPage, SplitTitle } from "@/components/landing/Sections";
import { IconArrowRight, IconCheck, IconWhatsapp } from "@/components/brand/icons";
import { RawuhMark, RawuhTile } from "@/components/brand/RawuhMark";
import { getReseller, getSiteContact } from "@/lib/marketing";
import type { TitledText } from "@/lib/site-content";

export const metadata: Metadata = {
  title: "Program Reseller | Rawuh",
  description: "Jadi mitra Rawuh: tawarkan undangan digital ke klienmu, untuk wedding organizer, vendor, percetakan, dan perorangan.",
};

function NumberedCards({ items }: { items: TitledText[] }) {
  return (
    <div className={styles.principles}>
      {items.map(({ title, text }, index) => <div key={title}><b>{String(index + 1).padStart(2, "0")}</b><h3>{title}</h3><p>{text}</p></div>)}
    </div>
  );
}

export default async function ResellerPage() {
  const [{ waLink }, content] = await Promise.all([getSiteContact(), getReseller()]);
  // The WhatsApp chat opens with the registration message already typed.
  const join = waLink ? `${waLink}?text=${encodeURIComponent(content.wa_message)}` : "/tentang#kontak";
  const external = waLink ? { target: "_blank", rel: "noreferrer" } : {};

  return (
    <MarketingPage current="reseller">
      <section className={styles.head} aria-labelledby="reseller-title">
        <Breadcrumb items={[["Beranda", "/"], ["Program Reseller"]]} />
        <div className={styles.aboutHead}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Program Reseller</p>
            <SplitTitle as="h1" id="reseller-title" className={styles.h1} lead={content.title_lead} mono={content.title_mono} />
          </div>
          <div style={{ display: "grid", gap: 24, justifyItems: "start" }}>
            <p className={styles.lead}>{content.lead}</p>
            <a href={join} className={base.btnPrimary} {...external}><IconWhatsapp size={16} /> Daftar jadi mitra</a>
          </div>
        </div>
      </section>

      <section className={base.section} aria-labelledby="audience-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Untuk siapa</p>
          <h2 id="audience-title" className={base.sectionTitle}>Cocok untuk usaha di sekitar hari bahagia.</h2>
        </div>
        <NumberedCards items={content.audiences} />
      </section>

      <section className={base.section} aria-labelledby="benefit-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Keuntungan</p>
          <SplitTitle id="benefit-title" className={base.splitInline} lead="Kamu fokus ke klien," mono="kami urus teknologinya." />
        </div>
        <NumberedCards items={content.benefits} />
        {content.terms.trim() && (
          <div style={{ marginTop: 32, padding: "20px 24px", border: "1px solid var(--rw-primary-border)", borderRadius: "var(--rw-radius-lg)", background: "var(--rw-primary-soft)" }}>
            <p className={base.eyebrow} style={{ marginBottom: 8 }}>Ketentuan & komisi</p>
            {content.terms.split(/\n\s*\n/).filter(p => p.trim()).map((paragraph, i) => (
              <p key={i} style={{ color: "var(--rw-ink-2)", lineHeight: 1.7, whiteSpace: "pre-line", marginTop: i ? 10 : 0 }}>{paragraph.trim()}</p>
            ))}
          </div>
        )}
      </section>

      <section className={base.section} aria-labelledby="steps-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Cara kerja</p>
          <h2 id="steps-title" className={base.sectionTitle}>Dari daftar sampai undangan terkirim.</h2>
        </div>
        <NumberedCards items={content.steps} />
      </section>

      <FaqSection waLink={waLink} items={content.faq} />

      <section className={base.section} style={{ borderBottom: 0 }} aria-labelledby="join-title">
        <div className={styles.partnerCta}>
          <div className={styles.partnerCopy}>
            <p className={styles.partnerKicker}>Gabung jadi mitra</p>
            <h2 id="join-title">{content.cta_heading}</h2>
            <p>Ceritakan usahamu ke tim kami. Penawaran harga mitra dan ketentuannya kami kirim lewat WhatsApp.</p>
            <ul className={styles.partnerPerks}>
              <li><IconCheck size={14} weight="bold" /> Tanya-tanya dulu, tanpa komitmen</li>
              <li><IconCheck size={14} weight="bold" /> Dibalas langsung oleh tim Rawuh</li>
            </ul>
            <div className={styles.partnerActions}>
              <a href={join} className={styles.partnerPrimary} {...external}><IconWhatsapp size={18} /> Daftar via WhatsApp</a>
              <Link href="/templates" className={styles.partnerGhost}>Lihat tema <IconArrowRight size={14} /></Link>
            </div>
          </div>
          {/* What the button does: WhatsApp opens with this message already typed. */}
          <div className={styles.partnerChat} aria-hidden="true">
            <div className={styles.partnerChatHead}><RawuhTile size={28} /><span><b>Rawuh</b><small>Tim kemitraan</small></span></div>
            <div className={styles.partnerBubble}>{content.wa_message}<small>Terisi otomatis</small></div>
            <div className={styles.partnerTyping}><i /><i /><i /></div>
          </div>
          <span className={styles.partnerMark} aria-hidden="true"><RawuhMark size={260} color="currentColor" door="currentColor" /></span>
        </div>
      </section>
    </MarketingPage>
  );
}
