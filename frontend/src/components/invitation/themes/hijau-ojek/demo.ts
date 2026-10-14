import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ratna", groom: "Sigit",
    brideFull: "Ratna Dewi", groomFull: "Sigit Prakoso",
    brideParents: "Putri Bapak Slamet & Ibu Tari", groomParents: "Putra Bapak Harto & Ibu Yani",
    bridePhoto: "/themes/img/a97.webp", groomPhoto: "/themes/img/a96.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-01-16T08:00:00+07:00",
  place: "Balai Kartini",
  address: "Jl. Gatot Subroto, Jakarta",
  stories: [
    { title: "Kampus UI → Kantin", date: "2019", body: "Order pertama: Sigit nebeng payung Ratna saat hujan." },
    { title: "Jakarta → Bandung", date: "2022", body: "Perjalanan jauh pertama. Macet 5 jam, ngobrol tanpa jeda." },
    { title: "Rumah → Pelaminan", date: "2026", body: "Tujuan akhir: lamaran diterima, rute seumur hidup dimulai." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-01-16T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Istiqlal", address: "Jakarta Pusat" },
    { name: "Resepsi", date: "2027-01-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Kartini", address: "Jl. Gatot Subroto" },
  ],
  gallery: ["/themes/img/a95.webp", "/themes/img/r76.webp", "/themes/img/r83.webp", "/themes/img/r80.webp"],
  gifts: [{ id: "demo-ewallet", type: "ewallet", ewallet_provider: "Dompet Digital", ewallet_number: "0812 1601 2027", account_name: "Ratna Dewi" }],
  guestName: "Bapak Joko Susilo & Keluarga",
});
