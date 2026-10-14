import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Putri", groom: "Dika",
    brideFull: "Putri Maharani", groomFull: "Dika Ramadhan",
    brideParents: "Putri Bapak Bagyo & Ibu Nur", groomParents: "Putra Bapak Hendra & Ibu Wiwik",
    bridePhoto: "/themes/img/a114.webp", groomPhoto: "/themes/img/a113.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T08:00:00+07:00",
  place: "Gedung Sabuga",
  address: "Jl. Tamansari, Bandung",
  stories: [
    { title: "Ketemu di Himpunan", date: "2019", body: "Pertama kenal saat rapat himpunan mahasiswa.", image: "/themes/img/r87.webp" },
    { title: "Resmi Jadian", date: "2021", body: "Resmi jadian setelah dua tahun berteman.", image: "/themes/img/r86.webp" },
    { title: "Lamaran di Lembang", date: "2026", body: "Lamaran sederhana di Lembang bersama keluarga.", image: "/themes/img/r89.webp" },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Salman ITB", address: "Bandung" },
    { name: "Resepsi", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Sabuga", address: "Jl. Tamansari, Bandung" },
  ],
  gallery: ["/themes/img/a111.webp", "/themes/img/a116.webp", "/themes/img/a117.webp", "/themes/img/a118.webp", "/themes/img/a115.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "1206 2027 88", account_name: "Putri Maharani" }],
  guestName: "Bapak Rahmat Hidayat & Keluarga",
});
