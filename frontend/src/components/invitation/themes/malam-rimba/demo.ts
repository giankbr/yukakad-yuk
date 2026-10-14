import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Arsen",
    note: "Di antara rimbun daun dan cahaya kecil, kami memilih untuk tumbuh bersama.",
    brideFull: "Kirana Maheswari, M.Ars.", groomFull: "Arsen Pradipta, S.T.",
    brideParents: "Putri dari Bapak Hendra Gunawan & Ibu Sinta", groomParents: "Putra dari Bapak Pradipta & Ibu Maya",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-12-12T16:00:00+07:00",
  place: "Rumah Kaca Dago",
  address: "Jl. Dago Pakar No. 9, Bandung",
  stories: [
    { date: "2018", title: "Studio Arsitektur", body: "Lembur bareng, maket yang sama, dua kepala yang beda." },
    { date: "2021", title: "Tanam Pohon", body: "Pacaran resmi sambil menanam pohon pertama di Dago." },
    { date: "2025", title: "Lamaran di Rumah Kaca", body: "Di bawah monstera raksasa, Arsen berlutut." },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-12-12T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Rumah Kaca Dago", address: "Jl. Dago Pakar No. 9, Bandung" },
    { name: "Resepsi", date: "2026-12-12T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Rumah Kaca Dago", address: "Jl. Dago Pakar No. 9, Bandung" },
  ],
  gallery: ["/themes/img/a87.webp", "/themes/img/a85.webp", "/themes/img/a86.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4455 6677 889", account_name: "Kirana Maheswari" },
    { id: "demo-kado", type: "address", address: "Jl. Dago Pakar No. 9, Bandung, Jawa Barat" },
  ],
  guestName: "Bapak Hendra Gunawan & Keluarga",
});
