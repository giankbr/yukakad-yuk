import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Dewa",
    note: "Semoga Tuhan Yang Maha Esa senantiasa melimpahkan kebahagiaan kepada kami berdua.",
    brideFull: "Ni Putu Ayu Lestari, S.Pd.", groomFull: "I Dewa Gede Arya Wibawa",
    brideParents: "Putri dari Bapak I Wayan Sudira & Ibu Ni Made Sari", groomParents: "Putra dari Bapak I Dewa Putu Oka & Ibu Dewa Ayu Rai",
    bridePhoto: "/themes/img/a62.webp", groomPhoto: "/themes/img/a60.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-09-06T09:00:00+08:00",
  place: "Griya Keluarga Dewa",
  address: "Br. Padangtegal, Gianyar, Ubud",
  stories: [
    { title: "Bertemu di Pura", date: "2018", body: "Saat upacara di Pura Desa, Ayu menari; Dewa lupa menabuh gamelan." },
    { title: "Jalan di Campuhan", date: "2021", body: "Pacaran pertama kali di Bukit Campuhan Ridge Walk." },
    { title: "Lamaran", date: "2025", body: "Keluarga Dewa datang melamar dengan sesajen lengkap." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2026-09-06T09:00:00+08:00", time: "09.00 – 11.00 WITA", venue: "Griya Keluarga Dewa", address: "Br. Padangtegal, Ubud, Gianyar" },
    { name: "Resepsi", date: "2026-09-06T18:00:00+08:00", time: "18.00 – 21.00 WITA", venue: "Pendopo Taman Ayu", address: "Jl. Raya Ubud, Gianyar, Bali" },
  ],
  gallery: ["/themes/img/a54.webp", "/themes/img/a64.webp", "/themes/img/a71.webp", "/themes/img/a73.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "Bank BPD Bali", account_number: "0101 2233 4455", account_name: "Ni Putu Ayu Lestari" },
    { id: "demo-kado", type: "address", address: "Jl. Raya Pengosekan No. 12, Ubud, Gianyar, Bali" },
  ],
  guestName: "Bapak I Wayan Sudira & Keluarga",
});
