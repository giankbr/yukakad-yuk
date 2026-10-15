// Product pages (/produk/[slug]). Defaults below; admins override per product via site-content "products".

type Pair = [string, string];
export type ProductContent = {
  slug: string;
  name: string;
  icon: string;
  headline: Pair;
  lead: string;
  price: string;
  image: string;
  primary: { label: string; href: string };
  secondary: { label: string; href: string };
  stats: Pair[];
  steps: Pair[];
  perks: Pair[];
};

export const PRODUCT_PERK_ICONS = ["user", "users", "calendar", "pin", "images", "music", "gift", "sparkle", "refresh", "link", "wifi", "download", "file", "mail", "truck", "qr", "globe", "video", "printer"] as const;

export const defaultProducts: ProductContent[] = [
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
];

const filled = (value: unknown): value is string => typeof value === "string" && value.trim() !== "";
const pairs = (value: unknown, fallback: Pair[]) => {
  const list = Array.isArray(value) ? value.filter((p): p is Pair => Array.isArray(p) && filled(p[0]) && filled(p[1])) : [];
  return list.length ? list : fallback;
};
const link = (value: unknown, fallback: { label: string; href: string }) => {
  const v = (value ?? {}) as Partial<{ label: string; href: string }>;
  return { label: filled(v.label) ? v.label : fallback.label, href: filled(v.href) ? v.href : fallback.href };
};

/** Overlay admin edits (matched by slug) on the default products. Empty fields keep the default. */
export function mergeProducts(items: unknown): ProductContent[] {
  const edits = Array.isArray(items) ? (items as Partial<ProductContent>[]) : [];
  return defaultProducts.map((base) => {
    const edit = edits.find((item) => item?.slug === base.slug);
    if (!edit) return base;
    const headline = Array.isArray(edit.headline) ? edit.headline : [];
    return {
      ...base,
      name: filled(edit.name) ? edit.name : base.name,
      lead: filled(edit.lead) ? edit.lead : base.lead,
      price: filled(edit.price) ? edit.price : base.price,
      image: filled(edit.image) ? edit.image : base.image,
      headline: [filled(headline[0]) ? headline[0] : base.headline[0], filled(headline[1]) ? headline[1] : base.headline[1]],
      primary: link(edit.primary, base.primary),
      secondary: link(edit.secondary, base.secondary),
      stats: pairs(edit.stats, base.stats),
      steps: pairs(edit.steps, base.steps),
      perks: pairs(edit.perks, base.perks),
    };
  });
}
