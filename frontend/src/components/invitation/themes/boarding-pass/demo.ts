import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Citra", groom: "Bagus",
    brideFull: "Citra Larasati", groomFull: "Bagus Mahotama",
    brideParents: "Putri Bapak Laras & Ibu Ketut", groomParents: "Putra Bapak Mahendra & Ibu Ayu",
    bridePhoto: "/themes/img/r34.webp", groomPhoto: "/themes/img/r35.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-10T08:00:00+08:00",
  place: "Hanggar Garden, Sanur",
  address: "Sanur, Denpasar",
  stories: [
    { date: "2021", title: "Boarding — Kenalan di bandara", body: "dua kursi bersebelahan, delay jadi berkah" },
    { date: "2022", title: "Lepas landas — Jadian", body: "menembus turbulensi LDR Jakarta–Denpasar" },
    { date: "2026", title: "Ketinggian jelajah — Lamaran", body: "stabil di ketinggian, cincin mendarat mulus" },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-10T08:00:00+08:00", time: "08.00 – 10.00 WITA", venue: "Kapel Taman Bali", address: "Denpasar" },
    { name: "Resepsi", date: "2027-10-10T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Hanggar Garden", address: "Sanur" },
  ],
  gallery: ["/themes/img/r33.webp", "/themes/img/r37.webp", "/themes/img/r38.webp", "/themes/img/r36.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "1010 2027 77", account_name: "Citra Larasati" }],
  guestName: "Bapak Surya Darmawan & Keluarga",
});
