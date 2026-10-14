// Shared server-side data + helpers for Rawuh marketing pages.
export const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export type Hero = { heading?: string; subheading?: string; cta_label?: string; cta_href?: string };
export type Kontak = { heading?: string; subheading?: string; whatsapp?: string };
export type FooterContent = { heading?: string; copyright?: string; instagram?: string };
export type Feature = { id: string; title: string; description: string; icon?: string };
export type Testimonial = { id: string; name: string; role?: string; quote: string; avatar_url?: string; is_sample?: boolean };
export type Template = { id: string; name: string; slug: string; category: string; preview_image?: string; preview_url?: string; is_premium: boolean };
export type Plan = { id: string; name: string; max_guests: number; has_watermark: boolean; custom_domain_allowed: boolean; payment_gateway_allowed: boolean; premium_templates_allowed?: boolean; price: number; duration_days?: number | null };

export const defaultTemplates: Template[] = [
  { id: "alyra", name: "Alyra", slug: "alyra", category: "Editorial", preview_url: "/invitation/demo?template=alyra", is_premium: false },
  { id: "weddings", name: "Weddings", slug: "weddings", category: "Modern", preview_url: "/invitation/demo?template=weddings", is_premium: false },
  { id: "veloria", name: "Veloria", slug: "veloria", category: "Editorial", preview_url: "/invitation/demo?template=veloria", is_premium: false },
];

export const defaultPlans: Plan[] = [
  { id: "free", name: "Mulai", max_guests: 100, has_watermark: true, custom_domain_allowed: false, payment_gateway_allowed: false, price: 0 },
  { id: "pro", name: "Rayakan", max_guests: 1000, has_watermark: false, custom_domain_allowed: true, payment_gateway_allowed: true, price: 149000, duration_days: 30 },
];

export const templateImages: Record<string, string> = {
  alyra: "/templates/alyra-preview.png",
  weddings: "/templates/weddings-preview.png",
  veloria: "/templates/veloria-preview.png",
};

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
  return template.preview_image || templateImages[template.slug];
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

export const products = [
  {
    slug: "undangan-website",
    name: "Undangan Website",
    icon: "globe",
    headline: ["Satu link,", "semua info acara."],
    lead: "Undangan website dengan nama tamu, RSVP, galeri, peta, dan amplop digital. Dibuat dari HP dalam 10 menit.",
    price: "Mulai dari paket gratis",
    image: "/rawuh/phone-kirana.webp",
    primary: { label: "Coba gratis", href: "/auth/register" },
    secondary: { label: "Lihat contoh", href: "/templates" },
    stats: [["10 mnt", "rata-rata waktu buat"], ["548", "tema siap pakai"], ["120rb+", "undangan terkirim"]],
    steps: [["Pilih tema", "Ratusan desain, bisa ganti warna & font."], ["Isi data acara", "Nama, tanggal, lokasi, foto — semua dari HP."], ["Bagikan link", "Kirim personal ke setiap tamu via WhatsApp."]],
    perks: [["user", "Nama tamu personal"], ["calendar", "RSVP & jumlah tamu"], ["pin", "Peta & rute"], ["images", "Galeri foto & video"], ["music", "Musik latar"], ["gift", "Amplop digital"]],
  },
  {
    slug: "video-ucapan-3d",
    name: "Video Ucapan 3D",
    icon: "video",
    headline: ["Undangan yang", "bergerak & bercerita."],
    lead: "Video 30 detik dengan animasi 3D, nama kalian, dan musik pilihan. Siap untuk story Instagram & status WhatsApp.",
    price: "Rp99rb / video",
    image: "/rawuh/product-video.webp",
    primary: { label: "Pesan video", href: "contact" },
    secondary: { label: "Lihat tema", href: "/templates" },
    stats: [["30 dtk", "durasi optimal story"], ["1080p", "kualitas HD vertikal"], ["24 jam", "jadi & siap kirim"]],
    steps: [["Pilih template", "Animasi 3D: amplop, buku, gerbang, bunga."], ["Upload foto", "Kami sesuaikan warna & teks dengan acaramu."], ["Unduh & bagikan", "MP4 untuk story, status, dan grup keluarga."]],
    perks: [["sparkle", "20+ template animasi"], ["user", "Nama & tanggal custom"], ["music", "Musik bebas royalti"], ["images", "Format 9:16 & 1:1"], ["refresh", "2x revisi gratis"], ["link", "Link ke undangan website"]],
  },
  {
    slug: "qr-checkin",
    name: "QR Check-in",
    icon: "qr",
    headline: ["Buku tamu", "tanpa antre."],
    lead: "Setiap tamu dapat QR unik di undangannya. Penerima tamu cukup scan dari HP — nama, rombongan, dan waktu datang tercatat otomatis.",
    price: "Termasuk di semua paket",
    image: "/rawuh/product-checkin.webp",
    primary: { label: "Coba gratis", href: "/auth/register" },
    secondary: { label: "Lihat harga", href: "/harga" },
    stats: [["3 dtk", "per tamu check-in"], ["0", "alat tambahan"], ["Live", "pantau dari dashboard"]],
    steps: [["Aktifkan check-in", "Satu toggle di dashboard undangan."], ["Tamu bawa QR", "QR muncul otomatis di undangan tiap tamu."], ["Scan di venue", "Pakai HP siapa saja, bisa beberapa meja."]],
    perks: [["qr", "Scan dari kamera HP"], ["users", "Multi penerima tamu"], ["user", "Layar sambutan nama tamu"], ["pin", "Info nomor meja"], ["wifi", "Tetap jalan saat offline"], ["download", "Ekspor kehadiran"]],
  },
  {
    slug: "undangan-cetak",
    name: "Undangan Cetak",
    icon: "printer",
    headline: ["Untuk yang", "tetap ingin dipegang."],
    lead: "Kartu undangan premium dengan desain senada tema website-mu, plus QR yang mengarah ke undangan digital. Cocok untuk orang tua & tamu kehormatan.",
    price: "Mulai Rp3.500 / lembar",
    image: "/rawuh/product-print.webp",
    primary: { label: "Pesan cetak", href: "contact" },
    secondary: { label: "Lihat tema", href: "/templates" },
    stats: [["50", "minimal pesanan"], ["5 hari", "produksi & kirim"], ["34", "provinsi terjangkau"]],
    steps: [["Pilih desain", "Otomatis senada dengan tema website."], ["Cek proof digital", "Revisi teks sampai yakin, gratis."], ["Kami cetak & kirim", "Dikemas rapi, sampai di rumahmu."]],
    perks: [["file", "Art paper 260 gsm"], ["sparkle", "Opsi foil emas"], ["qr", "QR ke undangan website"], ["mail", "Amplop & segel lilin"], ["user", "Label nama tamu"], ["truck", "Kirim ke seluruh Indonesia"]],
  },
] as const;

export type Product = (typeof products)[number];
