import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Daniel",
    note: "Sederhana saja: kamu, aku, dan hari-hari setelah ini.",
    brideFull: "Alya Rahmawati", groomFull: "Daniel Setiawan",
    brideParents: "Putri dari Bapak Surya Wijaya & Ibu Hana", groomParents: "Putra dari Bapak Setiawan & Ibu Linda",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-10-24T10:00:00+07:00",
  place: "Studio Linen",
  address: "Jl. Kemang Raya No. 7, Jakarta Selatan",
  stories: [
    { date: "2019", title: "Kantor yang Sama", body: "Satu divisi, meja bersebelahan, kopi yang sama." },
    { date: "2023", title: "Jalan Jauh", body: "Pindah kota bareng, bawa satu kardus dan satu kucing." },
    { date: "2025", title: "Ya", body: "Daniel bertanya di balkon. Alya menjawab sebelum selesai." },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-10-24T10:00:00+07:00", time: "10.00 – 11.00 WIB", venue: "Rumah Keluarga Wijaya", address: "Jl. Kemang Timur No. 21, Jakarta Selatan" },
    { name: "Resepsi", date: "2026-10-24T12:00:00+07:00", time: "12.00 – 15.00 WIB", venue: "Studio Linen", address: "Jl. Kemang Raya No. 7, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a78.webp", "/themes/img/a74.webp", "/themes/img/r88.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Bank Mandiri", account_number: "1230 0045 6789", account_name: "Alya Rahmawati" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Timur No. 21, Jakarta Selatan" },
  ],
  guestName: "Bapak Surya Wijaya & Keluarga",
});
