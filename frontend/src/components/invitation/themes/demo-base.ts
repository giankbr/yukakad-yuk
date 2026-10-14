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
