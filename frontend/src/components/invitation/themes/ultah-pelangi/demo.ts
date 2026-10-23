import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "",
    brideFull: "Kirana Ayu Lestari",
    brideParents: "Putri pertama dari Bapak Reza Pratama & Ibu Annisa Rahmadani",
    note: "Kirana genap empat tahun! Yuk datang membawa senyum paling cerah, kita warnai sore bersama.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-10-23T15:00:00+07:00",
  place: "Taman Bermain Awan Ceria",
  address: "Jl. Dago Atas No. 12, Ciburial, Cimenyan, Kabupaten Bandung",
  story: { title: "Cerita Kirana", body: "" },
  stories: [
    { date: "2023", title: "Hadiah setelah hujan", body: "Kirana lahir di sore hari, tepat ketika pelangi muncul di langit Bandung. Ayah langsung tahu nama yang cocok." },
    { date: "2025", title: "Krayon pertama", body: "Dinding kamar jadi kanvas pertama Kirana. Warna favoritnya? Semuanya, kata Kirana." },
    { date: "2027", title: "Empat tahun!", body: "Sekarang Kirana sudah bisa menyebut tujuh warna pelangi dan ingin merayakannya bersama semua teman." },
  ],
  events: [
    { name: "Pesta Pelangi Kirana", date: "2027-10-23T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Taman Bermain Awan Ceria", address: "Jl. Dago Atas No. 12, Ciburial, Cimenyan, Kabupaten Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "4370 2289 16", account_name: "Annisa Rahmadani" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Timur No. 31, Cibeunying Kaler, Bandung 40191" },
  ],
  guestName: "Adik Raffa & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kirana Ayu Lestari", nickname: "Kirana", birthDate: "2023-10-20T16:10:00+07:00", parents: "Putri pertama dari Bapak Reza Pratama & Ibu Annisa Rahmadani" },
    rundown: { items: [
      { time: "15.00", title: "Datang & ambil topi pelangi", note: "Setiap anak memilih satu warna" },
      { time: "15.20", title: "Melukis awan dan pelangi" },
      { time: "16.00", title: "Lomba balon warna-warni" },
      { time: "16.45", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju warna favoritmu! Semakin berwarna, semakin seru.", colors: ["#ef6f6c", "#f7cd5a", "#8fcf8a", "#6fb6e6", "#a58ad8"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Aki & Enin Rahmadani"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Kirana impikan.", items: [
      { id: "w1", name: "Set cat air anak", price: "± Rp120.000" },
      { id: "w2", name: "Buku cerita bergambar", price: "± Rp80.000", claimed_by: "Tante Sari" },
      { id: "w3", name: "Payung pelangi kecil", price: "± Rp95.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, tersedia tempat duduk teduh untuk orang tua di sekitar area bermain." },
      { q: "Bagaimana jika hujan?", a: "Acara dipindah ke aula beratap di samping taman. Mungkin malah ada pelangi!" },
    ] },
  },
});
