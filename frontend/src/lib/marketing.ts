// Shared server-side data + helpers for Rawuh marketing pages.
export const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export type Hero = { heading?: string; subheading?: string; cta_label?: string; cta_href?: string };
export type Kontak = { heading?: string; subheading?: string; whatsapp?: string };
export type FooterContent = { heading?: string; copyright?: string; instagram?: string; tiktok?: string };
export type Feature = { id: string; title: string; description: string; icon?: string };
export type Testimonial = { id: string; name: string; role?: string; quote: string; avatar_url?: string; is_sample?: boolean };
export type Template = { id: string; name: string; slug: string; category: string; preview_image?: string; preview_url?: string; is_premium: boolean };
export type Plan = { id: string; name: string; max_guests: number; has_watermark: boolean; custom_domain_allowed: boolean; payment_gateway_allowed: boolean; premium_templates_allowed?: boolean; price: number; duration_days?: number | null };

import { themeList } from "@/components/invitation/themes/registry";
import { mergeProducts } from "./products";
import { legalSection, mergeAbout, mergeLegal, type AboutContent, type LegalContent } from "./site-content";
import type { LegalDoc } from "./legal";

export const defaultTemplates: Template[] = [
  ...themeList.map(theme => ({
    id: theme.id, name: theme.name, slug: theme.id, category: theme.category,
    preview_image: `/themes/previews/${theme.id}.webp`, preview_url: `/invitation/demo?template=${theme.id}`, is_premium: theme.tier === "premium",
  })),
];

export const defaultPlans: Plan[] = [
  { id: "free", name: "Mulai", max_guests: 100, has_watermark: true, custom_domain_allowed: false, payment_gateway_allowed: false, price: 0 },
  { id: "pro", name: "Rayakan", max_guests: 1000, has_watermark: false, custom_domain_allowed: true, payment_gateway_allowed: true, price: 149000, duration_days: 30 },
];


export async function getJSON<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${path}`, { next: { revalidate: 60 } });
    if (!response.ok) return fallback;
    return response.json();
  } catch {
    return fallback;
  }
}

export async function getTemplates() {
  const result = await getJSON<{ items?: Template[] }>("/api/templates", {});
  return result.items?.length ? result.items : defaultTemplates;
}

export async function getPlans() {
  const result = await getJSON<{ items?: Plan[] }>("/api/public/plans", {});
  return (result.items?.length ? result.items : defaultPlans).slice().sort((a, b) => a.price - b.price);
}

export type LandingStat = { value: string; label: string };
export type FaqItem = { q: string; a: string };
export type Announcement = { enabled?: boolean; text?: string; label?: string; href?: string };

export const defaultStats: LandingStat[] = [
  { value: "120rb+", label: "undangan dibuat oleh pasangan dan keluarga di seluruh Indonesia." },
  { value: "500+", label: "tema siap pakai untuk pernikahan, khitan, aqiqah, hingga ulang tahun." },
  { value: "10 mnt", label: "rata-rata waktu dari pilih tema sampai undangan siap dikirim." },
  { value: "4.9/5", label: "rating dari 18.000+ ulasan pengguna di Google Play." },
];

export const defaultFaq: FaqItem[] = [
  { q: "Apakah bisa mencoba gratis?", a: "Bisa. Kamu dapat membuat dan melihat pratinjau undangan tanpa biaya. Pembayaran hanya diperlukan saat undangan siap dibagikan ke tamu." },
  { q: "Apakah ada batas jumlah tamu?", a: "Setiap paket punya kapasitas tamu yang berbeda. Lihat detailnya di halaman harga sebelum memilih paket." },
  { q: "Berapa lama proses pembuatannya?", a: "Rata-rata sekitar 10 menit: pilih tema, isi data acara, lalu bagikan link ke tamu." },
  { q: "Apa maksud masa aktif undangan?", a: "Masa aktif adalah lama link undanganmu bisa dibuka tamu. Setelah lewat, kamu tetap bisa memperpanjang dari dashboard." },
  { q: "Apakah tema bisa di-custom?", a: "Bisa. Ubah foto, teks, musik, dan section tambahan, lalu lihat pratinjaunya seketika." },
  { q: "Apakah tersedia program reseller?", a: "Ya. Vendor WO dan EO bisa menghubungi tim kami lewat WhatsApp untuk informasi program reseller." },
];

export const defaultAnnouncement: Announcement = {
  enabled: true,
  text: "Baru: Undangan Video 3D & QR Check-in untuk semua paket Premium",
  label: "Lihat sekarang",
  href: "/produk/video-ucapan-3d",
};

/** Landing blocks managed from Admin → Konten lainnya; each falls back to the defaults above when empty. */
export async function getLandingContent() {
  const [stats, faq, announcement] = await Promise.all([
    getJSON<{ items?: LandingStat[] }>("/api/public/site-content/stats", {}),
    getJSON<{ items?: FaqItem[] }>("/api/public/site-content/faq", {}),
    getJSON<Announcement>("/api/public/site-content/announcement", {}),
  ]);
  const statItems = (stats.items ?? []).filter((item) => item?.value?.trim() && item?.label?.trim());
  const faqItems = (faq.items ?? []).filter((item) => item?.q?.trim() && item?.a?.trim());
  const hasAnnouncement = typeof announcement.enabled === "boolean" || Boolean(announcement.text?.trim());
  return {
    stats: statItems.length ? statItems : defaultStats,
    faq: faqItems.length ? faqItems : defaultFaq,
    announcement: hasAnnouncement ? { ...defaultAnnouncement, ...announcement } : defaultAnnouncement,
  };
}

/** Contact + footer content shared by every marketing page. */
export async function getSiteContact() {
  const [kontak, footer] = await Promise.all([
    getJSON<Kontak>("/api/public/site-content/kontak", {}),
    getJSON<FooterContent>("/api/public/site-content/footer", {}),
  ]);
  const waLink = kontak.whatsapp ? `https://wa.me/${kontak.whatsapp.replace(/[^0-9]/g, "")}` : undefined;
  return { kontak, footer, waLink };
}

export function templatePreview(template: Template) {
  return template.preview_image || `/themes/previews/${template.slug}.webp`;
}

export function templateDemoHref(template: Template, names?: string) {
  const base = template.preview_url || `/invitation/demo?template=${encodeURIComponent(template.id)}`;
  if (!names) return base;
  return `${base}${base.includes("?") ? "&" : "?"}names=${encodeURIComponent(names)}`;
}

export function shortPrice(amount: number) {
  if (amount <= 0) return { value: "Gratis", unit: "" };
  if (amount % 1000 === 0) return { value: `${(amount / 1000).toLocaleString("id-ID")}rb`, unit: "Rp" };
  return { value: amount.toLocaleString("id-ID"), unit: "Rp" };
}

export function priceLabel(amount: number) {
  const price = shortPrice(amount);
  return price.unit ? `${price.unit}${price.value}` : price.value;
}

export function planPerks(plan: Plan) {
  const perks = [`Hingga ${plan.max_guests.toLocaleString("id-ID")} tamu`, "RSVP & buku ucapan", "Kirim via WhatsApp"];
  perks.push(plan.has_watermark ? "Dengan watermark Rawuh" : "Tanpa watermark");
  if (plan.custom_domain_allowed) perks.push("Domain pribadi .id");
  if (plan.premium_templates_allowed) perks.push("Akses tema Premium");
  if (plan.payment_gateway_allowed) perks.push("Amplop digital");
  if (plan.duration_days) perks.push(`Aktif ${plan.duration_days} hari`);
  return perks;
}

export function planHref(plan: Plan) {
  return plan.price > 0 ? `/auth/login?plan=${encodeURIComponent(plan.id)}` : "/auth/register";
}

/** Plan a template is unlocked by: premium templates need the cheapest paid plan. */
export function planForTemplate(template: Template, plans: Plan[]) {
  if (!template.is_premium) return plans[0];
  return plans.find(plan => plan.premium_templates_allowed) ?? plans.find(plan => plan.price > 0) ?? plans[plans.length - 1];
}

export { defaultProducts as products, type ProductContent as Product } from "./products";

// ---------------------------------------------------------------- Editable pages (admin → Halaman)

export async function getProducts() {
  const content = await getJSON<{ items?: unknown }>("/api/public/site-content/products", {});
  return mergeProducts(content.items);
}

export async function getAbout() {
  return mergeAbout(await getJSON<Partial<AboutContent>>("/api/public/site-content/about", {}));
}

export async function getLegal(doc: LegalDoc) {
  return mergeLegal(doc, await getJSON<LegalContent>(`/api/public/site-content/${legalSection(doc.slug)}`, {}));
}
