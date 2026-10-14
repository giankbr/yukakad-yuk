import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsa", groom: "Dion",
    brideFull: "Salsa Maulida", groomFull: "Dion Pradana",
    brideParents: "Putri Bapak Maul & Ibu Ikah", groomParents: "Putra Bapak Pram & Ibu Lies",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T08:00:00+07:00",
  place: "Sudirman Grand Ballroom",
  address: "Jl. Sudirman, Bandung",
  stories: [
    { title: "Buka rekening kenalan", date: "2020", body: "Satu bootcamp finansial, beda meja, satu tujuan." },
    { title: "Auto-debit perhatian", date: "2022", body: "Resmi pacaran. Setoran rutin: kabar pagi & malam." },
    { title: "Kantong dikunci", date: "2026", body: "Lamaran diterima. Dana cinta tidak bisa ditarik lagi." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Salman ITB, Bandung", address: "Jl. Ganesha No. 7, Bandung" },
    { name: "Resepsi", date: "2027-06-19T11:30:00+07:00", time: "11.30 – 14.30 WIB", venue: "Sudirman Grand Ballroom, Bandung", address: "Jl. Sudirman, Bandung" },
  ],
  gallery: ["/themes/img/r94.webp", "/themes/img/r92.webp", "/themes/img/r93.webp"],
  gifts: [{ id: "demo-bank", type: "bank", bank_name: "Bank Kantong", account_number: "1906 2027 00", account_name: "Salsa Maulida" }],
  guestName: "Bapak Rahmat Hakim & Keluarga",
});
