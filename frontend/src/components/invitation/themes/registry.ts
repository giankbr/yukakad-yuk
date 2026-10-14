// Generated from the Rawuh design file. Theme ids are stable: they are stored as invitations.template_id.
import type { ComponentType } from "react";
import type { InvitationData } from "../types";
import type { ThemeProps } from "./kit";

export type ThemeMeta = { id: string; name: string; group: "utama" | "koleksi" | "brand" | "web"; category: string; tier: "free" | "premium"; description: string };

export const themeList: ThemeMeta[] = [
  { id: "marketplace", name: "Marketplace", group: "utama", category: "Belanja", tier: "premium", description: "Undangan bergaya aplikasi belanja: paket cinta, lacak perjalanan, dan ulasan tamu." },
  { id: "oranye", name: "Oranye", group: "utama", category: "Belanja", tier: "premium", description: "Nuansa promo oranye yang meriah dengan voucher kehadiran." },
  { id: "streaming", name: "Streaming", group: "utama", category: "Hiburan", tier: "premium", description: "Undangan ala serial streaming: episode kisah, jadwal tayang, dan ulasan penonton." },
  { id: "jawa", name: "Jawa Keraton", group: "utama", category: "Adat Jawa", tier: "premium", description: "Adat Jawa klasik cokelat-emas dengan gunungan dan aksara." },
  { id: "rumah-gadang", name: "Rumah Gadang", group: "koleksi", category: "Adat Minang", tier: "premium", description: "Adat Minang · Merah · Songket" },
  { id: "bali-kuning", name: "Bali Kuning", group: "koleksi", category: "Adat Bali", tier: "premium", description: "Adat Bali · Kuning · Kamboja" },
  { id: "syari-zamrud", name: "Syari Zamrud", group: "koleksi", category: "Syari", tier: "free", description: "Syari · Tanpa Foto · Hijau" },
  { id: "lavender-air", name: "Lavender Air", group: "koleksi", category: "Watercolor", tier: "premium", description: "Watercolor · Ungu · Ilustrasi" },
  { id: "linen-putih", name: "Linen Putih", group: "koleksi", category: "Minimalis", tier: "free", description: "Minimalist · Putih · Tipografi" },
  { id: "sketsa-tangan", name: "Sketsa Tangan", group: "koleksi", category: "Hand Drawn", tier: "free", description: "Hand Drawn · Cream · Line Art" },
  { id: "malam-rimba", name: "Malam Rimba", group: "koleksi", category: "Elegan", tier: "premium", description: "Elegant · Hitam · Botanical" },
  { id: "pastel-flat", name: "Pastel Flat", group: "koleksi", category: "Ilustrasi", tier: "free", description: "Flat · Pink · Ilustrasi Lucu" },
  { id: "hijau-ojek", name: "Hijau Ojek", group: "brand", category: "Aplikasi", tier: "premium", description: "Undangan bergaya Hijau Ojek yang unik dan personal." },
  { id: "pesan-antar", name: "Pesan-Antar", group: "brand", category: "Aplikasi", tier: "premium", description: "Undangan bergaya Pesan-Antar yang unik dan personal." },
  { id: "arena-legenda", name: "Arena Legenda", group: "brand", category: "Unik", tier: "premium", description: "Undangan bergaya Arena Legenda yang unik dan personal." },
  { id: "kanal-video", name: "Video", group: "brand", category: "Hiburan", tier: "premium", description: "Undangan bergaya Video yang unik dan personal." },
  { id: "repositori", name: "Repositori", group: "brand", category: "Unik", tier: "premium", description: "Undangan bergaya Repositori yang unik dan personal." },
  { id: "pemutar-musik", name: "Musik", group: "brand", category: "Hiburan", tier: "premium", description: "Undangan bergaya Musik yang unik dan personal." },
  { id: "playlist", name: "Playlist", group: "brand", category: "Hiburan", tier: "premium", description: "Undangan bergaya Playlist yang unik dan personal." },
  { id: "chat-hijau", name: "Chat Hijau", group: "web", category: "Sosial Media", tier: "free", description: "Undangan bergaya Chat Hijau yang unik dan personal." },
  { id: "feed-foto", name: "Feed Foto", group: "web", category: "Sosial Media", tier: "free", description: "Undangan bergaya Feed Foto yang unik dan personal." },
  { id: "video-vertikal", name: "Video Vertikal", group: "web", category: "Sosial Media", tier: "free", description: "Undangan bergaya Video Vertikal yang unik dan personal." },
  { id: "kencan", name: "Kencan", group: "web", category: "Sosial Media", tier: "free", description: "Undangan bergaya Kencan yang unik dan personal." },
  { id: "peta-rute", name: "Peta", group: "web", category: "Aplikasi", tier: "free", description: "Undangan bergaya Peta yang unik dan personal." },
  { id: "surel", name: "Surel", group: "web", category: "Aplikasi", tier: "free", description: "Undangan bergaya Surel yang unik dan personal." },
  { id: "dokumen", name: "Dokumen", group: "web", category: "Aplikasi", tier: "free", description: "Undangan bergaya Dokumen yang unik dan personal." },
  { id: "rapat-video", name: "Rapat Video", group: "web", category: "Aplikasi", tier: "free", description: "Undangan bergaya Rapat Video yang unik dan personal." },
  { id: "boarding-pass", name: "Boarding Pass", group: "web", category: "Perjalanan", tier: "free", description: "Undangan bergaya Boarding Pass yang unik dan personal." },
  { id: "tiket-kereta", name: "Tiket Kereta", group: "web", category: "Perjalanan", tier: "free", description: "Undangan bergaya Tiket Kereta yang unik dan personal." },
  { id: "game-retro", name: "Game Retro", group: "web", category: "Unik", tier: "free", description: "Undangan bergaya Game Retro yang unik dan personal." },
  { id: "koran", name: "Koran", group: "web", category: "Unik", tier: "free", description: "Undangan bergaya Koran yang unik dan personal." },
  { id: "dompet-digital", name: "Dompet Digital", group: "web", category: "Fintech", tier: "free", description: "Undangan bergaya Dompet Digital yang unik dan personal." },
  { id: "saku-biru", name: "Saku Biru", group: "web", category: "Fintech", tier: "free", description: "Undangan bergaya Saku Biru yang unik dan personal." },
  { id: "poin-ungu", name: "Poin Ungu", group: "web", category: "Fintech", tier: "free", description: "Undangan bergaya Poin Ungu yang unik dan personal." },
  { id: "kantong-oranye", name: "Kantong Oranye", group: "web", category: "Fintech", tier: "free", description: "Undangan bergaya Kantong Oranye yang unik dan personal." },
  { id: "kursi-kereta", name: "Kursi Kereta", group: "web", category: "Perjalanan", tier: "free", description: "Undangan bergaya Kursi Kereta yang unik dan personal." },
  { id: "paket-liburan", name: "Paket Liburan", group: "web", category: "Perjalanan", tier: "free", description: "Undangan bergaya Paket Liburan yang unik dan personal." },
  { id: "rencana-perjalanan", name: "Rencana Perjalanan", group: "web", category: "Perjalanan", tier: "free", description: "Undangan bergaya Rencana Perjalanan yang unik dan personal." },
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

export function isTheme(id?: string): id is string {
  return Boolean(id && id in loaders);
}

export async function loadTheme(id: string) {
  const entry = loaders[id];
  const [mod, demo] = await Promise.all([entry.component(), entry.demo()]);
  return { Theme: mod.default, demo: demo.demo };
}
