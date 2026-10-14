import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Maya", groom: "Kevin",
    brideFull: "Maya Anggraini", groomFull: "Kevin Mahendra",
    brideParents: "Putri Bapak Anggara & Ibu Westi", groomParents: "Putra Bapak Hendra & Ibu Rosa",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r29.webp",
  },
  eventLabel: "Menikah",
  date: "2027-05-09T08:00:00+07:00",
  place: "The Mansion, Dago Pakar",
  address: "Bandung",
  stories: [
    { title: "Match", date: "2022", body: "Halo! Akhirnya match juga. Kopi minggu ini?" },
    { title: "Kencan pertama", date: "2022", body: "Boleh. Tapi aku pilih tempatnya ya?" },
    { title: "Lamaran", date: "2026", body: "5 tahun kemudian: tempatnya pelaminan?" },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-09T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Trans Studio", address: "Bandung" },
    { name: "Resepsi", date: "2027-05-09T11:30:00+07:00", time: "11.30 – 14.30 WIB", venue: "The Mansion, Dago Pakar" },
  ],
  gallery: ["/themes/img/r27.webp", "/themes/img/r26.webp", "/themes/img/r82.webp", "/themes/img/r85.webp", "/themes/img/r81.webp", "/themes/img/r84.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0905 2027 66", account_name: "Maya Anggraini" }],
  guestName: "Kak Sarah Oktaviani & Partner",
});
