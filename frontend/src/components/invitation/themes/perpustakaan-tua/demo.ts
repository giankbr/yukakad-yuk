import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anindya", groom: "Raka",
    brideFull: "Anindya Paramitha Kusuma, S.Hum.",
    groomFull: "Raka Adiwangsa Putra, M.A.",
    brideParents: "Putri pertama dari\nBapak Hendro Kusumo & Ibu Ratna Wulandari",
    groomParents: "Putra kedua dari\nBapak Agus Adiwangsa & Ibu Lestari Hadiningrum",
    bridePhoto: "/themes/img/a77.webp",
    groomPhoto: "/themes/img/a76.webp",
    note: "Dua pembaca yang dulu berebut satu buku, kini menulis bab-bab berikutnya bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T10:00:00+07:00",
  place: "Gedung Arsip Nasional",
  address: "Jl. Gajah Mada No. 111, Krukut, Taman Sari, Jakarta Barat",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Maret 2019", title: "Satu buku, dua peminjam", body: "Di lantai tiga perpustakaan kampus, kami sama-sama meraih satu-satunya eksemplar novel yang sama. Raka mengalah; Anindya berjanji mengembalikannya dalam seminggu." },
    { date: "2021", title: "Catatan di pinggir halaman", body: "Kami mulai bertukar buku dan meninggalkan catatan kecil di pinggir halaman. Lama-lama catatan itu lebih panjang dari bukunya." },
    { date: "Desember 2026", title: "Lamaran di rak puisi", body: "Di toko buku bekas langganan kami, Raka menyelipkan cincin di antara halaman kumpulan puisi kesukaan Anindya." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-09-18T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Ruang Baca Utama, Gedung Arsip Nasional", address: "Jl. Gajah Mada No. 111, Krukut, Taman Sari, Jakarta Barat" },
    { name: "Resepsi", date: "2027-09-18T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Taman Belakang, Gedung Arsip Nasional", address: "Jl. Gajah Mada No. 111, Krukut, Taman Sari, Jakarta Barat" },
  ],
  gallery: ["/themes/img/a132.webp", "/themes/img/a124.webp", "/themes/img/a101.webp", "/themes/img/a74.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5271 0388 19", account_name: "Anindya Paramitha Kusuma" },
    { id: "demo-kado", type: "address", address: "Jl. Cikini Raya No. 73, Cikini, Menteng, Jakarta Pusat 10330" },
  ],
  guestName: "Ibu Sekar Ayuningtyas & Keluarga",
  guestTable: "Rak 7",
  extras: {
    quote: { text: "Mencintai bukanlah saling memandang, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Keluarga inti & sahabat dekat" },
      { time: "11.00", title: "Mengisi buku tamu", note: "Setiap tamu menulis satu kalimat untuk kami" },
      { time: "18.30", title: "Resepsi dibuka" },
      { time: "19.30", title: "Pembacaan puisi & tukar buku", note: "Bawa satu buku kesayangan, pulang dengan buku lain" },
    ] },
    dressCode: { note: "Nuansa perpustakaan tua: merah marun, hijau botol, cokelat kenari, atau krem.", colors: ["#6b1f1f", "#24503a", "#5a3620", "#efe4cc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Keluarga Besar Kusumo", "Keluarga Besar Adiwangsa", "Komunitas Baca Kamisan"] },
    faq: { items: [
      { q: "Apakah wajib membawa buku?", a: "Tidak wajib. Bila berkenan, bawalah satu buku bekas kesayangan untuk acara tukar buku." },
      { q: "Di mana tempat parkir?", a: "Parkir tersedia di halaman Gedung Arsip Nasional dan di gedung parkir seberang jalan." },
    ] },
  },
});
