import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Mira", groom: "Bagas",
    note: "Kata orang cinta itu rumit. Kata kami: tinggal bilang iya.",
    brideFull: "Mira Anindya", groomFull: "Bagas Saputra",
    brideParents: "Putri Bapak Anton & Ibu Rini", groomParents: "Putra Bapak Saputra & Ibu Dian",
    bridePhoto: "/themes/img/a88.webp", groomPhoto: "/themes/img/a89.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-02-14T09:00:00+07:00",
  place: "Taman Bungkul Hall",
  address: "Jl. Raya Darmo, Surabaya",
  stories: [
    { date: "2021", title: "Ketemu di Kafe", body: "Mira pesan matcha, Bagas salah ambil gelasnya." },
    { date: "2023", title: "Jadian", body: "Di bioskop, filmnya jelek, tapi malamnya seru." },
    { date: "2025", title: "Lamaran", body: "Bagas bawa balon 100 biji dan satu cincin." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-02-14T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Al-Falah", address: "Jl. Raya Darmo No. 137, Surabaya" },
    { name: "Pesta", date: "2027-02-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Taman Bungkul Hall", address: "Jl. Raya Darmo, Surabaya" },
  ],
  gallery: ["/themes/img/a91.webp", "/themes/img/a90.webp", "/themes/img/a92.webp", "/themes/img/a93.webp", "/themes/img/a88.webp", "/themes/img/a89.webp"],
  gifts: [
    { id: "demo-jago", type: "bank", bank_name: "Bank Jago", account_number: "5099 1234 5678", account_name: "Mira Anindya" },
    { id: "demo-kado", type: "address", address: "Jl. Darmo Permai III No. 4, Surabaya, Jawa Timur" },
  ],
  guestName: "Keluarga Bapak Anton",
});
