import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Dewi", groom: "Arya",
    brideFull: "Dewi Anggraini", groomFull: "Arya Wiratama",
    brideParents: "Putri ke-2 Bpk. Suryadi & Ibu Lestari", groomParents: "Putra ke-1 Bpk. Gunawan & Ibu Dian",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-11-11T08:00:00+07:00",
  place: "Hotel Savoy Homann",
  address: "Jl. Asia Afrika No.112, Bandung",
  stories: [
    { date: "2019", title: "Pertemuan pertama di perpustakaan kampus", body: "Dewi: Kak, pensilnya masih ada?\nArya: Masih kok. Tapi bolehkah aku tukar dengan nomor HP-mu?" },
    { date: "2021", title: "Resmi berpacaran setelah 2 tahun berteman", body: "" },
    { date: "2025", title: "Lamaran di Kawah Putih, Ciwidey", body: "Arya: Dewi, mau checkout hatiku selamanya?\nDewi: Checkout sekarang!" },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-11-11T08:00:00+07:00", time: "08.00–10.00 WIB", venue: "Masjid Pusdai", address: "Jl. Diponegoro No.63, Bandung" },
    { name: "Resepsi", date: "2026-11-11T11:00:00+07:00", time: "11.00–14.00 WIB", venue: "Hotel Savoy Homann", address: "Jl. Asia Afrika No.112" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a30.webp", "/themes/img/a31.webp", "/themes/img/a32.webp", "/themes/img/a33.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "130 0012 3456", account_name: "Dewi A." },
    { id: "demo-alamat", type: "address", account_name: "Dewi Anggraini | (+62) 812-3456-7890", address: "Jl. Dago Asri No. 11, Coblong, Bandung 40135" },
  ],
  guestName: "Ibu Ratna Sari & Keluarga",
});
