import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, MarketingPage, SplitTitle } from "@/components/landing/Sections";
import { ThemeBrowser, type BrowserTemplate } from "@/components/landing/ThemeBrowser";
import { IconAward, IconGift, IconImages, IconMusic, IconPin, IconWhatsapp } from "@/components/brand/icons";
import { getPlans, getSiteContact, getTemplates, planForTemplate, priceLabel, templateDemoHref, templatePreview } from "@/lib/marketing";

export const metadata: Metadata = {
  title: "Galeri Tema | Rawuh",
  description: "Jelajahi tema undangan digital Rawuh, coba langsung dengan nama kalian, lalu pakai untuk acaramu.",
};

export default async function TemplatesPage() {
  const [templates, plans, { waLink }] = await Promise.all([getTemplates(), getPlans(), getSiteContact()]);
  const items: BrowserTemplate[] = templates.map(template => ({
    id: template.id,
    slug: template.slug,
    name: template.name,
    category: template.category || "Umum",
    eventType: template.event_type,
    preview: templatePreview(template),
    demoHref: templateDemoHref(template),
    isPremium: template.is_premium,
    price: priceLabel(planForTemplate(template, plans).price),
  }));
  const featured = templates.find(template => template.is_premium && templatePreview(template)) ?? templates.find(templatePreview) ?? templates[0];
  const categories = new Set(items.map(item => item.category)).size;
  const premiumCount = items.filter(item => item.isPremium).length;

  return (
    <MarketingPage current="tema">
      <section className={styles.head} style={{ borderBottom: 0 }} aria-labelledby="tema-title">
        <Breadcrumb items={[["Beranda", "/"], ["Galeri Tema"]]} />
        <div className={styles.temaHead}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Galeri tema · {items.length} desain</p>
            <SplitTitle as="h1" id="tema-title" className={styles.h1} lead={items.length >= 100 ? "Ratusan tema," : "Tema pilihan,"} mono="satu yang paling kamu." />
            <p className={styles.lead} style={{ maxWidth: 560 }}>Semua tema bisa diganti warna, font, dan foto sesukamu. Coba langsung dengan nama kalian sebelum memutuskan.</p>
          </div>
          <div className={styles.temaStats}>
            <div><strong>{items.length}</strong><small>tema aktif</small></div>
            <div><strong>{categories}</strong><small>kategori</small></div>
            <div><strong>{premiumCount}</strong><small>tema premium</small></div>
          </div>
        </div>
        <ThemeBrowser templates={items} />
      </section>

      {featured && (
        <section className={base.section} style={{ borderTop: "1px solid var(--rw-border-warm)" }} aria-labelledby="featured-title">
          <div className={styles.featured}>
            <Link href={`/templates/${featured.slug}`} className={styles.featuredVisual}>
              <span className={styles.editorPick}><IconAward size={12} /> Pilihan Editor</span>
              {templatePreview(featured) && <Image src={templatePreview(featured)!} alt={`Pratinjau tema ${featured.name}`} fill sizes="(max-width: 900px) 100vw, 560px" style={{ objectPosition: "top" }} />}
            </Link>
            <div className={styles.featuredCopy}>
              <p className={base.eyebrow}>Tema minggu ini</p>
              <h2 id="featured-title">{featured.name}<span className={`${styles.badge} ${featured.is_premium ? "" : styles.badgeNeutral}`}>{featured.is_premium ? "Premium" : featured.category}</span></h2>
              <p className={styles.lead} style={{ fontSize: 17 }}>Tipografi rapi dan tata letak yang tenang, siap diisi foto dan cerita kalian. Semua bagian undangan bisa diatur dari HP.</p>
              <div className={styles.miniFeatures}>
                <span><IconImages size={14} /> Galeri foto</span>
                <span><IconMusic size={14} /> Musik latar</span>
                <span><IconPin size={14} /> Peta lokasi</span>
                <span><IconGift size={14} /> Amplop digital</span>
              </div>
              <div className={styles.actions}>
                <Link href={`/auth/register?template=${encodeURIComponent(featured.id)}`} className={base.btnPrimary}>Pakai tema ini</Link>
                <a href={templateDemoHref(featured)} target="_blank" rel="noreferrer" className={base.btnOutline}>Lihat demo</a>
              </div>
            </div>
          </div>
        </section>
      )}

      <section className={base.section} style={{ borderBottom: 0 }}>
        <div className={styles.darkCta}>
          <div>
            <p className={base.eyebrow}>Desain custom</p>
            <h2><span>Belum ketemu yang pas?</span><span>Kami buatkan.</span></h2>
            <p>Kirim referensi warna &amp; mood, desainer kami selesaikan dalam 3 hari kerja. Mulai Rp499rb.</p>
          </div>
          <div>
            <a href={waLink ?? "/tentang#kontak"} className={base.btnPrimary} {...(waLink ? { target: "_blank", rel: "noreferrer" } : {})}>Request desain</a>
            {waLink && <a href={waLink} className={styles.btnDarkOutline} target="_blank" rel="noreferrer"><IconWhatsapp size={14} /> Chat admin</a>}
          </div>
        </div>
      </section>
    </MarketingPage>
  );
}
