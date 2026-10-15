// Server-safe helpers for theme demo data (no "use client": demo data is passed from server pages).
import type { InvitationData } from "../types";

type DeepPartial<T> = { [K in keyof T]?: T[K] extends Array<infer U> ? U[] : T[K] extends object ? DeepPartial<T[K]> : T[K] };

const base: InvitationData = {
  couple: { bride: "Rina", groom: "Bima", note: "Dua cerita yang akhirnya menemukan rumah yang sama." },
  eventLabel: "Pernikahan",
  date: "2026-12-12T08:00:00+07:00",
  place: "Gedung Graha Sarana",
  address: "Jl. Gatot Subroto Kav. 12, Jakarta",
  story: { title: "Kisah kami", body: "Bertemu di kelas desain, bertumbuh bersama, dan kini memulai babak baru." },
  events: [
    { name: "Akad Nikah", date: "2026-12-12T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja, Kebayoran Baru" },
    { name: "Resepsi", date: "2026-12-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Graha Sarana", address: "Jl. Gatot Subroto Kav. 12, Jakarta" },
  ],
  gallery: [],
  gifts: [{ id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "1234567890", account_name: "Rina Maharani" }],
  guestName: "Bapak Budi Santoso & Keluarga",
  guestTable: "12",
  // Sample extra sections so every demo shows what can be switched on from the dashboard.
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.30", title: "Sungkeman" },
      { time: "11.00", title: "Resepsi dibuka", note: "Kirab & pembukaan" },
      { time: "12.30", title: "Foto bersama", note: "Per rombongan" },
    ] },
    dressCode: { note: "Nuansa earth tone. Batik dipersilakan.", colors: ["#a3b18a", "#dad7cd", "#b08968", "#6b705c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2026-12-12T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hartono", "Kel. Besar Bpk. Suryadi", "Keluarga Besar Trah Mangunkusumo", "Rekan kerja PT Sinar Abadi"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan terdekat dari lokasi.", items: [
      { name: "Hotel Santika Premiere", detail: "± 800 m dari gedung · kode promo RINABIMA" },
      { name: "Parkir & shuttle", detail: "Parkir basement Graha Sarana, shuttle tiap 15 menit" },
    ] },
    wishlist: { items: [
      { id: "w1", name: "Set peralatan masak", price: "± Rp1.200.000" },
      { id: "w2", name: "Rice cooker digital", price: "± Rp850.000", claimed_by: "Dinda" },
      { id: "w3", name: "Voucher bulan madu", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Tentu, anak-anak sangat diterima. Kursi tambahan tersedia di area keluarga." },
      { q: "Apakah tersedia parkir?", a: "Ada parkir basement gratis untuk tamu undangan." },
      { q: "Sampai jam berapa acaranya?", a: "Resepsi berlangsung hingga pukul 14.00 WIB." },
    ] },
  },
};

/** Theme demo data: the base sample merged with the theme's own design copy. */
export function makeDemo(overrides: DeepPartial<InvitationData> = {}): InvitationData {
  return {
    ...base,
    ...overrides,
    couple: { ...base.couple, ...(overrides.couple ?? {}) },
    story: { ...base.story, ...(overrides.story ?? {}) },
  } as InvitationData;
}
