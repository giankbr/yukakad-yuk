import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tara", groom: "Gilang",
    note: "Kami nggak jago bikin puisi, jadi kami gambar saja.",
    brideFull: "Tara Kusuma", groomFull: "Gilang Ramadhan",
    brideParents: "anak Bapak Kusuma & Ibu Wati", groomParents: "anak Bapak Ramadhan & Ibu Sri",
    bridePhoto: "/themes/img/a79.webp", groomPhoto: "/themes/img/a81.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-11-07T09:00:00+07:00",
  place: "Halaman Rumah Tara",
  address: "Jl. Ijen No. 12, Malang",
  stories: [
    { date: "2017", title: "Satu Bangku", body: "SMA, kelas XI, Gilang minjam pulpen terus." },
    { date: "2021", title: "Jarak Jauh", body: "Tara ke Jogja, Gilang di Malang. Tiap malam telepon." },
    { date: "2025", title: "Nembak Lagi", body: "Gilang nembak pakai komik buatan sendiri, 12 halaman." },
  ],
  events: [
    { name: "Akad", date: "2026-11-07T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Al-Ikhlas", address: "Jl. Pahlawan No. 3, Malang" },
    { name: "Makan-makan", date: "2026-11-07T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Halaman Rumah Tara", address: "Jl. Ijen No. 12, Malang" },
  ],
  gallery: ["/themes/img/a80.webp", "/themes/img/a75.webp", "/themes/img/a82.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0011 2233 4455", account_name: "Tara Kusuma" },
    { id: "demo-kado", type: "address", address: "Jl. Ijen No. 12, Malang, Jawa Timur" },
  ],
  guestName: "Kak Rina & Partner",
});
