import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, FinalCta, MarketingPage, SplitTitle } from "@/components/landing/Sections";
import { ThemeCard, TryNameForm } from "@/components/landing/ThemeBrowser";
import { IconArrowRight, IconCalendar, IconCheck, IconImages, IconQr } from "@/components/brand/icons";
import { getPlans, getTemplates, planForTemplate, planHref, priceLabel, shortPrice, templateDemoHref, templatePreview } from "@/lib/marketing";

async function findTemplate(slug: string) {
  const templates = await getTemplates();
  return { templates, template: templates.find(item => item.slug === slug || item.id === slug) };
}

export async function generateMetadata({ params }: PageProps<"/templates/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  const { template } = await findTemplate(slug);
  if (!template) return {};
  return { title: `Tema ${template.name} | Rawuh`, description: `Tema undangan digital ${template.name} (${template.category}). Lihat demo dan coba dengan nama kalian.` };
}

const sections = [
  ["Sampul", "Nama tamu tampil di halaman pembuka."],
  ["Mempelai", "Profil, foto, dan cerita kalian."],
  ["Acara & peta", "Jadwal acara dengan rute Google Maps."],
  ["Galeri", "Foto prewedding dan momen favorit."],
  ["RSVP & amplop", "Konfirmasi hadir, ucapan, dan hadiah."],
];

export default async function TemplateDetailPage({ params }: PageProps<"/templates/[slug]">) {
  const { slug } = await params;
  const [{ templates, template }, plans] = await Promise.all([findTemplate(slug), getPlans()]);
  if (!template) notFound();
  const plan = planForTemplate(template, plans);
  const price = shortPrice(plan.price);
  const preview = templatePreview(template);
  const demoHref = templateDemoHref(template);
  const similar = templates.filter(item => item.id !== template.id)
    .sort((a, b) => Number(b.category === template.category) - Number(a.category === template.category)).slice(0, 4);

  return (
    <MarketingPage current="tema">
      <section className={styles.head} style={{ paddingTop: 40 }} aria-labelledby="detail-title">
        <Breadcrumb items={[["Galeri Tema", "/templates"], [template.category || "Umum", "/templates"], [template.name]]} />
        <div className={styles.detail}>
          <div className={styles.detailMain}>
            {preview
              ? <Image src={preview} alt={`Pratinjau tema ${template.name}`} fill sizes="(max-width: 900px) 100vw, 640px" preload unoptimized={!preview.startsWith("/")} />
              : <span className={styles.placeholder} aria-hidden>{template.name.slice(0, 1)}</span>}
          </div>
          <div className={styles.detailInfo}>
            <h1 id="detail-title">{template.name}<span className={`${styles.badge} ${template.is_premium ? "" : styles.badgeNeutral}`}>{template.is_premium ? "Premium" : "Gratis"}</span></h1>
            <div className={styles.meta}><span>{template.category || "Umum"}</span><span>Bisa ganti warna, font &amp; foto</span></div>
            <p className={styles.lead} style={{ fontSize: 16 }}>Tema {template.name} dirancang rapi untuk HP maupun laptop. Isi nama, acara, foto, dan cerita kalian — pratinjau berubah seketika.</p>
            <dl className={styles.specs}>
              <div><dt>Kategori</dt><dd>{template.category || "Umum"}</dd></div>
              <div><dt>Tampilan</dt><dd>HP &amp; desktop</dd></div>
            </dl>
            <TryNameForm demoHref={demoHref} />
            <div className={styles.planBox}>
              <small>{plan.price > 0 ? `Termasuk paket ${plan.name}` : `Bisa dipakai di paket ${plan.name}`}</small>
              <div><strong>{price.unit && <span>{price.unit}</span>}{price.value}</strong><em>{plan.price > 0 ? "sekali bayar" : "tanpa biaya"}</em></div>
            </div>
            <div className={styles.stack}>
              <Link href={`/auth/register?template=${encodeURIComponent(template.id)}`} className={base.btnPrimary}>Pakai tema ini — gratis coba</Link>
              <a href={demoHref} target="_blank" rel="noreferrer" className={base.btnOutline}>Buka demo live</a>
            </div>
            <ul className={styles.checks}>
              <li><span><IconImages size={12} /></span>Galeri foto</li>
              <li><span><IconCalendar size={12} /></span>RSVP, ucapan &amp; amplop digital</li>
              <li><span><IconQr width={12} height={12} /></span>QR check-in tamu</li>
              {plan.duration_days && <li><span><IconCheck size={12} /></span>Aktif {plan.duration_days} hari</li>}
            </ul>
            {plan.price > 0 && <Link href={planHref(plan)} className={styles.textLink}>Lihat detail paket {plan.name} <IconArrowRight size={14} /></Link>}
          </div>
        </div>
      </section>

      <section className={base.section} style={{ background: "var(--rw-surface-2)" }} aria-labelledby="sections-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Isi undangan</p>
          <SplitTitle id="sections-title" className={base.splitInline} lead={`${sections.length} bagian,`} mono="satu gulir." />
        </div>
        <ol className={styles.sections}>
          {sections.map(([title, desc], index) => <li key={title}><b>{String(index + 1).padStart(2, "0")}</b><h3>{title}</h3><p>{desc}</p></li>)}
        </ol>
      </section>

      {similar.length > 0 && (
        <section className={base.section} aria-labelledby="similar-title">
          <div className={styles.rowHead}>
            <h2 id="similar-title" className={base.sectionTitle}>Tema serupa</h2>
            <Link href="/templates" className={styles.textLink}>Lihat semua tema <IconArrowRight size={14} /></Link>
          </div>
          <div className={styles.similar}>
            {similar.map(item => (
              <ThemeCard key={item.id} template={{
                id: item.id, slug: item.slug, name: item.name, category: item.category || "Umum", preview: templatePreview(item),
                demoHref: templateDemoHref(item), isPremium: item.is_premium, price: priceLabel(planForTemplate(item, plans).price),
              }} />
            ))}
          </div>
        </section>
      )}

      <FinalCta />
    </MarketingPage>
  );
}
