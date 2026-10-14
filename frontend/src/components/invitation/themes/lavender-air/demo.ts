import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Reza",
    note: "Aku tak punya rencana besar, hanya satu: menghabiskan sisa hari bersamamu.",
    brideFull: "Nadia Putri Anjani", groomFull: "Reza Pratama Hidayat",
    brideParents: "Putri dari Bapak Hartono & Ibu Dewi Lestari", groomParents: "Putra dari Bapak Hidayat & Ibu Ratna",
    bridePhoto: "/themes/img/a65.webp", groomPhoto: "/themes/img/a59.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-10-10T09:00:00+07:00",
  place: "Kebun Raya Bogor",
  address: "Jl. Ir. H. Juanda No. 13, Bogor",
  stories: [
    { title: "Satu Kelas Daring", date: "2020", body: "Berkenalan saat kuliah online, kamera Reza selalu mati." },
    { title: "Kencan Kebun Raya", date: "2022", body: "Pertama kali bertemu langsung, hujan deras, satu payung." },
    { title: "Lamaran", date: "2025", body: "Reza melamar di taman anggrek dengan buket lavender." },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-10-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Kebun Raya Bogor", address: "Jl. Ir. H. Juanda No. 13, Bogor" },
    { name: "Resepsi", date: "2026-10-10T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Taman Lavender Bogor", address: "Jl. Pajajaran No. 88, Bogor" },
  ],
  gallery: ["/themes/img/a55.webp", "/themes/img/a69.webp", "/themes/img/a68.webp", "/themes/img/a67.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0987 6543 21", account_name: "Nadia Putri Anjani" },
    { id: "demo-kado", type: "address", address: "Jl. Pakuan No. 5, Bogor, Jawa Barat" },
  ],
  guestName: "Ibu Dewi Lestari & Keluarga",
});
