import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sari", groom: "Fadli",
    note: "Seperti pepatah Minang: seiya sekata, senasib sepenanggungan — semoga kami begitu hingga tua.",
    brideFull: "Sari Ramadhani, S.E.", groomFull: "Fadli Rahman, S.T.",
    brideParents: "Putri dari Bapak Rusli Chaniago & Ibu Yulia Sari", groomParents: "Putra dari Bapak H. Syafrudin & Ibu Elfida",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-08-15T08:00:00+07:00",
  place: "Rumah Gadang Keluarga",
  address: "Koto Gadang, Agam, Bukittinggi",
  stories: [
    { title: "Bertemu di Pasar Ateh", date: "2019", body: "Sari jual kain songket, Fadli pura-pura beli tiga kali." },
    { title: "Ngobrol di Jam Gadang", date: "2022", body: "Resmi berpacaran di bawah Jam Gadang saat hujan." },
    { title: "Lamaran Adat", date: "2025", body: "Keluarga Fadli datang membawa sirih pinang: lamaran diterima." },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-08-15T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Raya Bukittinggi", address: "Jl. Sudirman No. 1, Bukittinggi" },
    { name: "Resepsi Adat Minang", date: "2026-08-15T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Rumah Gadang Keluarga", address: "Koto Gadang, Agam, Sumatera Barat" },
  ],
  gallery: ["/themes/img/a56.webp", "/themes/img/a66.webp", "/themes/img/a61.webp", "/themes/img/a70.webp"],
  gifts: [
    { id: "demo-nagari", type: "bank", bank_name: "Bank Nagari", account_number: "1234 5678 9012", account_name: "Sari Ramadhani" },
    { id: "demo-kado", type: "address", address: "Jl. Panorama No. 8, Bukittinggi, Sumatera Barat" },
  ],
  guestName: "Bapak Rusli Chaniago & Keluarga",
});
