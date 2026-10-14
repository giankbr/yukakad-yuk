import type { Metadata } from "next";
import { AnnouncementBar, SiteFooter, SiteHeader } from "@/components/landing/SiteChrome";
import { ThemeGallery } from "@/components/landing/TemplateInteractions";
import styles from "@/app/landing.module.css";

export const metadata: Metadata = {
  title: "Tema Undangan Digital | Rawuh",
  description: "Jelajahi semua tema undangan digital Rawuh, lihat demonya, dan temukan yang paling cocok untuk acaramu.",
};

type Template = {
  id: string;
  name: string;
  slug: string;
  category: string;
  preview_image?: string;
  preview_url?: string;
  is_premium: boolean;
};

const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";
const previewBySlug: Record<string, string> = {
  alyra: "/templates/alyra-preview.png",
  weddings: "/templates/weddings-preview.png",
  veloria: "/templates/veloria-preview.png",
};
const fallbackTemplates: Template[] = [
  { id: "alyra", name: "Alyra", slug: "alyra", category: "Editorial", is_premium: false },
  { id: "weddings", name: "Weddings", slug: "weddings", category: "Modern", is_premium: false },
  { id: "veloria", name: "Veloria", slug: "veloria", category: "Editorial", is_premium: false },
];

async function getTemplates(): Promise<Template[]> {
  try {
    const response = await fetch(`${API_BASE}/api/templates`, { next: { revalidate: 60 } });
    if (!response.ok) return fallbackTemplates;
    const body: { items?: Template[] } = await response.json();
    return body.items?.length ? body.items : fallbackTemplates;
  } catch {
    return fallbackTemplates;
  }
}

export default async function TemplatesPage() {
  const templates = await getTemplates();
  return (
    <main className={styles.page}>
      <a className={styles.skip} href="#konten">Lewati navigasi</a>
      <AnnouncementBar />
      <SiteHeader current="tema" />
      <div className={styles.rail} id="konten">
        <section className={styles.pageHero} aria-labelledby="tema-title">
          <p className={styles.eyebrow}>Tema</p>
          <h1 id="tema-title"><span>Tema untuk setiap</span><span>momen berharga.</span></h1>
          <p className={styles.lead}>Pilih tema, lihat demonya langsung, lalu pakai untuk acaramu. Semua bisa diubah dari HP.</p>
        </section>
        <section className={styles.section}>
          <ThemeGallery title="Cari tema yang kamu banget." templates={templates.map(template => ({
            id: template.id,
            name: template.name,
            category: template.category || "Umum",
            preview: template.preview_image || previewBySlug[template.slug],
            demoHref: template.preview_url || `/invitation/demo?template=${encodeURIComponent(template.id)}`,
            isPremium: template.is_premium,
          }))} />
        </section>
      </div>
      <SiteFooter />
    </main>
  );
}
