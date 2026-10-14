import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Rendi",
    brideFull: "Salma Hayati", groomFull: "Rendi Pratama",
    brideParents: "Putri Bapak Hasan & Ibu Umi", groomParents: "Putra Bapak Pratama & Ibu Lina",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a102.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-03-21T08:00:00+07:00",
  place: "Grand Ballroom Santika",
  address: "Jl. Kapten Maulana Lubis, Medan",
  stories: [
    { title: "Pesanan dibuat", date: "2018", body: "Bertemu di kedai kopi Jl. Setiabudi, Medan." },
    { title: "Dikemas dengan cinta", date: "2021", body: "Resmi berpacaran setelah 3 tahun jadi teman ngopi." },
    { title: "Dalam perjalanan", date: "2026", body: "Lamaran diterima. Kurir cinta menuju tujuan akhir." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-21T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Agung Medan", address: "Jl. Pangeran Diponegoro, Medan" },
    { name: "Resepsi", date: "2027-03-21T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "Grand Ballroom Santika, Medan", address: "Jl. Kapten Maulana Lubis, Medan" },
  ],
  gallery: ["/themes/img/a101.webp", "/themes/img/a100.webp", "/themes/img/r78.webp", "/themes/img/r79.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2103 2027 11", account_name: "Salma Hayati" },
    { id: "demo-addr", type: "address", address: "Jl. Setiabudi No. 88, Medan Selayang" },
  ],
  guestName: "Ibu Sari Wulandari & Keluarga",
});
