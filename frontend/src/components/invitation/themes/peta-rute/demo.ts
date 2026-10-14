import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Galih",
    brideFull: "Laras Wulandari, S.Ars.", groomFull: "Galih Prasetya, M.M.",
    brideParents: "Putri Bapak Wulan & Ibu Harti", groomParents: "Putra Bapak Pras & Ibu Yayuk",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-13T08:00:00+07:00",
  place: "Gedung Graha",
  address: "Solo",
  stories: [
    { title: "Titik awal", date: "2020", body: "Bertemu di kereta Solo–Jogja, duduk bersebelahan." },
    { title: "Belok kiri ke hati", date: "2023", body: "Resmi berpacaran. Rute digabung permanen." },
    { title: "Hampir sampai", date: "2026", body: "Lamaran di Ngarsopuro Night Market." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-13T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Gedung Graha", address: "Solo" },
    { name: "Resepsi", date: "2027-06-13T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Graha", address: "Solo" },
  ],
  gallery: ["/themes/img/r62.webp", "/themes/img/r64.webp", "/themes/img/r61.webp", "/themes/img/r63.webp", "/themes/img/r65.webp", "/themes/img/r70.webp"],
  gifts: [{ id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "1306 2027 12", account_name: "Laras Wulandari" }],
  guestName: "Bapak Widodo Santoso & Keluarga",
});
