import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Evan",
    brideFull: "Zahra Amelia", groomFull: "Evan Pratama",
    brideParents: "Putri Bapak Amir & Ibu Lia", groomParents: "Putra Bapak Tono & Ibu Rahma",
    bridePhoto: "/themes/img/r21.webp", groomPhoto: "/themes/img/r22.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-11T08:00:00+07:00",
  place: "Plataran Senayan",
  address: "Jakarta",
  stories: [
    { title: "FYP-an pertama", date: "2022", body: "Video Zahra lewat di beranda Evan, langsung follow." },
    { title: "Duet pertama kami", date: "2023", body: "Duet lagu favorit, komentar penuh shipper." },
    { title: "Dia nembak di live", date: "2025", body: "Evan menyatakan perasaan saat siaran langsung." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-11T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Agung Al-Azhar" },
    { name: "Resepsi", date: "2027-04-11T18:00:00+07:00", time: "18.00 – 21.00 WIB", venue: "Plataran Senayan", address: "Jakarta" },
  ],
  gallery: ["/themes/img/r18.webp", "/themes/img/r19.webp", "/themes/img/r20.webp", "/themes/img/r23.webp", "/themes/img/r25.webp", "/themes/img/r24.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "1104 2027 33", account_name: "Zahra Amelia" }],
  guestName: "Kak Nadya Paramita & Keluarga",
});
