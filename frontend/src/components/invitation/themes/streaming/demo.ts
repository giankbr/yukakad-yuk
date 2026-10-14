import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Damar",
    brideFull: "Sekar Ayuningtyas", groomFull: "Damar Wicaksono",
    brideParents: "Putri dari Bpk. Harjono & Ibu Sri", groomParents: "Putra dari Bpk. Sutrisno & Ibu Wening",
    bridePhoto: "/themes/img/a36.webp", groomPhoto: "/themes/img/a35.webp",
    note: "Dua jiwa dari Kotagede dan Bantul, dipertemukan oleh hujan di Malioboro. Saksikan episode final mereka: janji suci di hadapan keluarga dan sahabat.",
  },
  eventLabel: "Pernikahan",
  date: "2026-06-20T08:00:00+07:00",
  place: "Ndalem Pujokusuman",
  address: "Jl. Brigjen Katamso No.45, Yogyakarta",
  stories: [
    { date: "2019", title: "Hujan di Malioboro", body: "Berteduh di emperan toko yang sama, berbagi satu payung.", image: "/themes/img/a39.webp" },
    { date: "2021", title: "Kopi & Jarak Jauh", body: "Damar kerja di Jakarta, Sekar di Jogja. Video call tiap malam.", image: "/themes/img/a37.webp" },
    { date: "2025", title: "Lamaran di Prambanan", body: "Di bawah langit senja Prambanan, Damar berlutut.", image: "/themes/img/a38.webp" },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-06-20T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Ndalem Pujokusuman", address: "Jl. Brigjen Katamso No.45, Yogyakarta" },
    { name: "Resepsi", date: "2026-06-20T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Royal Ambarrukmo", address: "Jl. Laksda Adisucipto No.81, Sleman" },
  ],
  gallery: ["/themes/img/a34.webp", "/themes/img/a41.webp", "/themes/img/a43.webp", "/themes/img/a44.webp", "/themes/img/a42.webp", "/themes/img/a40.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0123 4567 89", account_name: "Sekar A." },
    { id: "demo-kado", type: "address", address: "Jl. Kemasan No. 20, Kotagede, Yogyakarta" },
  ],
  guestName: "Bapak Andi Pratama & Keluarga",
});
