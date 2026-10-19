// Generated from the Rawuh design file. Theme ids are stable: they are stored as invitations.template_id.
import type { ComponentType } from "react";
import type { InvitationData } from "../types";
import type { ThemeProps } from "./kit";
import { freshDemo } from "./demo-base";

export type ThemeMeta = { id: string; name: string; group: "utama" | "koleksi" | "brand" | "web"; category: string; tier: "free" | "premium"; description: string };

export const themeList: ThemeMeta[] = [
  { id: "marketplace", name: "Marketplace", group: "utama", category: "Belanja", tier: "premium", description: "Undangan bergaya aplikasi belanja: paket cinta, lacak perjalanan, dan ulasan tamu." },
  { id: "oranye", name: "Oranye", group: "utama", category: "Belanja", tier: "premium", description: "Nuansa promo oranye yang meriah dengan voucher kehadiran." },
  { id: "streaming", name: "Streaming", group: "utama", category: "Hiburan", tier: "premium", description: "Undangan ala serial streaming: episode kisah, jadwal tayang, dan ulasan penonton." },
  { id: "jawa", name: "Jawa Keraton", group: "utama", category: "Adat Jawa", tier: "premium", description: "Adat Jawa klasik cokelat-emas dengan gunungan dan aksara." },
  { id: "rumah-gadang", name: "Rumah Gadang", group: "koleksi", category: "Adat Minang", tier: "premium", description: "Adat Minang merah-emas dengan motif songket dan siluet rumah gadang." },
  { id: "bali-kuning", name: "Bali Kuning", group: "koleksi", category: "Adat Bali", tier: "premium", description: "Adat Bali kuning keemasan dengan bunga kamboja dan gapura candi bentar." },
  { id: "syari-zamrud", name: "Syari Zamrud", group: "koleksi", category: "Syari", tier: "free", description: "Syari hijau zamrud tanpa foto, berisi doa dan ornamen geometris." },
  { id: "lavender-air", name: "Lavender Air", group: "koleksi", category: "Cat Air", tier: "premium", description: "Cat air ungu lembut dengan ilustrasi bunga dan polaroid." },
  { id: "linen-putih", name: "Linen Putih", group: "koleksi", category: "Minimalis", tier: "free", description: "Minimalis putih bersih yang mengandalkan tipografi." },
  { id: "sketsa-tangan", name: "Sketsa Tangan", group: "koleksi", category: "Gambar Tangan", tier: "free", description: "Gambar tangan di kertas krem, gaya buku tempel dengan coretan tinta." },
  { id: "malam-rimba", name: "Malam Rimba", group: "koleksi", category: "Elegan", tier: "premium", description: "Elegan hitam-emas dengan dedaunan dan kunang-kunang." },
  { id: "pastel-flat", name: "Pastel Flat", group: "koleksi", category: "Ilustrasi", tier: "free", description: "Ilustrasi datar pastel merah muda yang lucu dan ceria." },
  { id: "hijau-ojek", name: "Hijau Ojek", group: "brand", category: "Aplikasi", tier: "premium", description: "Ala aplikasi ojek online: rute cinta, perjalanan, dan bintang untuk pengantin." },
  { id: "pesan-antar", name: "Pesan-Antar", group: "brand", category: "Aplikasi", tier: "premium", description: "Ala aplikasi pesan-antar: menu acara, status pengiriman, dan voucher." },
  { id: "arena-legenda", name: "Arena Legenda", group: "brand", category: "Unik", tier: "premium", description: "Ala gim arena: pilih hero, rank pasangan, dan toko item hadiah." },
  { id: "kanal-video", name: "Video", group: "brand", category: "Hiburan", tier: "premium", description: "Ala kanal video: episode kisah, tayangan premiere, dan kolom komentar." },
  { id: "repositori", name: "Repositori", group: "brand", category: "Unik", tier: "premium", description: "Ala repositori kode: riwayat commit, kontribusi, dan diskusi." },
  { id: "pemutar-musik", name: "Musik", group: "brand", category: "Hiburan", tier: "premium", description: "Ala pemutar musik: daftar lagu acara, artis, dan pemutar mini." },
  { id: "playlist", name: "Playlist", group: "brand", category: "Hiburan", tier: "premium", description: "Ala playlist: antrean acara, kilas balik tahunan, dan pemutar mini." },
  { id: "chat-hijau", name: "Chat Hijau", group: "web", category: "Sosial Media", tier: "free", description: "Ala aplikasi chat: obrolan berdua, grup keluarga, dan ucapan tamu." },
  { id: "feed-foto", name: "Feed Foto", group: "web", category: "Sosial Media", tier: "free", description: "Ala feed foto: sorotan cerita, unggahan galeri, dan suka dari tamu." },
  { id: "video-vertikal", name: "Video Vertikal", group: "web", category: "Sosial Media", tier: "free", description: "Ala video vertikal: siaran premiere, hadiah, dan komentar tamu." },
  { id: "kencan", name: "Kencan", group: "web", category: "Sosial Media", tier: "free", description: "Ala aplikasi kencan: profil berdua, match, dan riwayat obrolan." },
  { id: "peta-rute", name: "Peta", group: "web", category: "Aplikasi", tier: "free", description: "Ala aplikasi peta: titik lokasi, rute perjalanan, dan ulasan tamu." },
  { id: "surel", name: "Surel", group: "web", category: "Aplikasi", tier: "free", description: "Ala kotak masuk surel: undangan sebagai email lengkap dengan lampiran." },
  { id: "dokumen", name: "Dokumen", group: "web", category: "Aplikasi", tier: "free", description: "Ala halaman dokumen: properti acara, daftar periksa, dan komentar." },
  { id: "rapat-video", name: "Rapat Video", group: "web", category: "Aplikasi", tier: "free", description: "Ala rapat video: ubin peserta, agenda, dan obrolan rapat." },
  { id: "boarding-pass", name: "Boarding Pass", group: "web", category: "Perjalanan", tier: "free", description: "Ala boarding pass: penerbangan cinta, gerbang, dan barcode tamu." },
  { id: "tiket-kereta", name: "Tiket Kereta", group: "web", category: "Perjalanan", tier: "free", description: "Ala tiket kereta: rute perjalanan, stasiun, dan jadwal keberangkatan." },
  { id: "game-retro", name: "Game Retro", group: "web", category: "Unik", tier: "free", description: "Ala gim retro piksel: karakter, level, dan toko item." },
  { id: "koran", name: "Koran", group: "web", category: "Unik", tier: "free", description: "Ala koran klasik: berita utama, kolom acara, dan iklan baris." },
  { id: "dompet-digital", name: "Dompet Digital", group: "web", category: "Keuangan", tier: "free", description: "Ala dompet digital: saldo cinta, riwayat transaksi, dan struk." },
  { id: "saku-biru", name: "Saku Biru", group: "web", category: "Keuangan", tier: "free", description: "Ala aplikasi bank: PIN masuk, transfer kasih, dan mutasi." },
  { id: "poin-ungu", name: "Poin Ungu", group: "web", category: "Keuangan", tier: "free", description: "Ala aplikasi poin: misi, tukar poin, dan tingkat keanggotaan." },
  { id: "kantong-oranye", name: "Kantong Oranye", group: "web", category: "Keuangan", tier: "free", description: "Ala kantong tabungan: target bersama, isi kantong, dan anggota." },
  { id: "kursi-kereta", name: "Kursi Kereta", group: "web", category: "Perjalanan", tier: "free", description: "Ala pemesanan kursi kereta: denah gerbong dan tiket tamu." },
  { id: "paket-liburan", name: "Paket Liburan", group: "web", category: "Perjalanan", tier: "free", description: "Ala paket liburan: rencana perjalanan, pesanan, dan voucher." },
  { id: "rencana-perjalanan", name: "Rencana Perjalanan", group: "web", category: "Perjalanan", tier: "free", description: "Ala aplikasi perjalanan: itinerary harian, penginapan, dan peta." },
];

type ThemeModule = { default: ComponentType<ThemeProps> };
type DemoModule = { demo: InvitationData };

const loaders: Record<string, { component: () => Promise<ThemeModule>; demo: () => Promise<DemoModule> }> = {
  "marketplace": { component: () => import("./marketplace"), demo: () => import("./marketplace/demo") },
  "oranye": { component: () => import("./oranye"), demo: () => import("./oranye/demo") },
  "streaming": { component: () => import("./streaming"), demo: () => import("./streaming/demo") },
  "jawa": { component: () => import("./jawa"), demo: () => import("./jawa/demo") },
  "rumah-gadang": { component: () => import("./rumah-gadang"), demo: () => import("./rumah-gadang/demo") },
  "bali-kuning": { component: () => import("./bali-kuning"), demo: () => import("./bali-kuning/demo") },
  "syari-zamrud": { component: () => import("./syari-zamrud"), demo: () => import("./syari-zamrud/demo") },
  "lavender-air": { component: () => import("./lavender-air"), demo: () => import("./lavender-air/demo") },
  "linen-putih": { component: () => import("./linen-putih"), demo: () => import("./linen-putih/demo") },
  "sketsa-tangan": { component: () => import("./sketsa-tangan"), demo: () => import("./sketsa-tangan/demo") },
  "malam-rimba": { component: () => import("./malam-rimba"), demo: () => import("./malam-rimba/demo") },
  "pastel-flat": { component: () => import("./pastel-flat"), demo: () => import("./pastel-flat/demo") },
  "hijau-ojek": { component: () => import("./hijau-ojek"), demo: () => import("./hijau-ojek/demo") },
  "pesan-antar": { component: () => import("./pesan-antar"), demo: () => import("./pesan-antar/demo") },
  "arena-legenda": { component: () => import("./arena-legenda"), demo: () => import("./arena-legenda/demo") },
  "kanal-video": { component: () => import("./kanal-video"), demo: () => import("./kanal-video/demo") },
  "repositori": { component: () => import("./repositori"), demo: () => import("./repositori/demo") },
  "pemutar-musik": { component: () => import("./pemutar-musik"), demo: () => import("./pemutar-musik/demo") },
  "playlist": { component: () => import("./playlist"), demo: () => import("./playlist/demo") },
  "chat-hijau": { component: () => import("./chat-hijau"), demo: () => import("./chat-hijau/demo") },
  "feed-foto": { component: () => import("./feed-foto"), demo: () => import("./feed-foto/demo") },
  "video-vertikal": { component: () => import("./video-vertikal"), demo: () => import("./video-vertikal/demo") },
  "kencan": { component: () => import("./kencan"), demo: () => import("./kencan/demo") },
  "peta-rute": { component: () => import("./peta-rute"), demo: () => import("./peta-rute/demo") },
  "surel": { component: () => import("./surel"), demo: () => import("./surel/demo") },
  "dokumen": { component: () => import("./dokumen"), demo: () => import("./dokumen/demo") },
  "rapat-video": { component: () => import("./rapat-video"), demo: () => import("./rapat-video/demo") },
  "boarding-pass": { component: () => import("./boarding-pass"), demo: () => import("./boarding-pass/demo") },
  "tiket-kereta": { component: () => import("./tiket-kereta"), demo: () => import("./tiket-kereta/demo") },
  "game-retro": { component: () => import("./game-retro"), demo: () => import("./game-retro/demo") },
  "koran": { component: () => import("./koran"), demo: () => import("./koran/demo") },
  "dompet-digital": { component: () => import("./dompet-digital"), demo: () => import("./dompet-digital/demo") },
  "saku-biru": { component: () => import("./saku-biru"), demo: () => import("./saku-biru/demo") },
  "poin-ungu": { component: () => import("./poin-ungu"), demo: () => import("./poin-ungu/demo") },
  "kantong-oranye": { component: () => import("./kantong-oranye"), demo: () => import("./kantong-oranye/demo") },
  "kursi-kereta": { component: () => import("./kursi-kereta"), demo: () => import("./kursi-kereta/demo") },
  "paket-liburan": { component: () => import("./paket-liburan"), demo: () => import("./paket-liburan/demo") },
  "rencana-perjalanan": { component: () => import("./rencana-perjalanan"), demo: () => import("./rencana-perjalanan/demo") },
};

/** Themes that render their own music button (the page then skips the generic <MusicPlayer>). */
export const themesWithOwnMusic = new Set(["jawa"]);

/** Theme used for invitations whose template is missing or retired. */
export const FALLBACK_THEME = "linen-putih";

export function isTheme(id?: string): id is string {
  return Boolean(id && id in loaders);
}

export async function loadTheme(id: string) {
  const entry = loaders[id];
  const [mod, demo] = await Promise.all([entry.component(), entry.demo()]);
  return { Theme: mod.default, demo: freshDemo(demo.demo) };
}
