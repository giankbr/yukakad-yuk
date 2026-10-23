import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana Larasati", groom: "Orkes Lembayung",
    brideFull: "Kirana Larasati", groomFull: "Orkes Kampung Lembayung",
    brideParents: "Penyanyi & penulis lagu dari Yogyakarta. Membawakan lagu-lagu dari album perdananya, \"Pulang ke Kali\".",
    groomParents: "Dua belas musisi kampung: keroncong, gitar, kendang, dan suling. Tampil tanpa honor untuk malam ini.",
    bridePhoto: "/themes/img/a127.webp", groomPhoto: "/themes/img/a133.webp",
    note: "Setiap tiket yang kamu ambil adalah satu buku baru untuk anak-anak di Taman Baca Pelita.",
  },
  eventLabel: "Konser Amal Nada untuk Pelita",
  date: "2027-08-21T16:00:00+07:00",
  place: "Panggung Terbuka Taman Kenari",
  address: "Jl. Kenari No. 12, Muja Muju, Umbulharjo, Yogyakarta",
  story: { title: "Untuk apa konser ini", body: "" },
  stories: [
    { date: "2019", title: "Satu Rak Buku", body: "Taman Baca Pelita lahir dari satu rak buku di teras rumah warga di pinggir kali. Sore hari, anak-anak datang membaca sambil menunggu orang tuanya pulang kerja." },
    { date: "2025", title: "Atap yang Bocor", body: "Kini ada 140 anak yang rutin datang, tetapi bangunannya sempit dan atapnya bocor setiap musim hujan. Banyak buku rusak sebelum sempat dibaca." },
    { date: "2027", title: "Malam Ini", body: "Seluruh hasil donasi dan tiket konser dipakai untuk memperbaiki ruang baca, menambah 1.000 buku cerita, dan membiayai kelas membaca gratis selama setahun." },
  ],
  events: [
    { name: "Bazar Buku & Open Gate", date: "2027-08-21T16:00:00+07:00", time: "16.00 – 18.30 WIB", venue: "Halaman Taman Kenari", address: "Jl. Kenari No. 12, Muja Muju, Umbulharjo, Yogyakarta" },
    { name: "Konser Amal", date: "2027-08-21T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Panggung Terbuka Taman Kenari", address: "Jl. Kenari No. 12, Muja Muju, Umbulharjo, Yogyakarta" },
  ],
  gallery: ["/themes/img/a129.webp", "/themes/img/a137.webp", "/themes/img/a126.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0029 0102 4471 503", account_name: "Perkumpulan Taman Baca Pelita" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "DANA", ewallet_number: "0812 2790 4416", account_name: "Panitia Nada untuk Pelita" },
    { id: "demo-buku", type: "address", address: "Sekretariat Taman Baca Pelita, Jl. Kenari No. 12, Umbulharjo, Yogyakarta 55165 (donasi buku layak baca)" },
  ],
  guestName: "Mas Dimas Prasetyo & Teman",
  guestTable: "Tribun B",
  extras: {
    quote: { text: "Musik tidak bisa mengubah dunia sendirian. Tetapi ia bisa mengumpulkan orang-orang yang mau mengubahnya.", source: "Panitia Nada untuk Pelita" },
    rundown: { items: [
      { time: "16.00", title: "Open gate & bazar buku bekas", note: "Bawa satu buku cerita, dapat stiker konser" },
      { time: "18.30", title: "Dongeng untuk anak-anak", note: "Bersama relawan Taman Baca Pelita" },
      { time: "19.00", title: "Orkes Kampung Lembayung" },
      { time: "20.15", title: "Kirana Larasati", note: "Penampil utama" },
      { time: "21.30", title: "Lelang gitar & penyerahan donasi" },
    ] },
    dressCode: { note: "Bebas dan nyaman. Kaus putih atau batik santai, siapkan jas hujan tipis bila mendung.", colors: ["#ff6b4a", "#ffc94a", "#2ec4b6", "#2a2160"] },
    guestPass: { note: "Tunjukkan kode ini di gerbang. Satu kode berlaku untuk jumlah tamu yang dikonfirmasi." },
    rsvpDietary: { label: "Butuh kursi prioritas atau akses kursi roda? (opsional)" },
    faq: { items: [
      { q: "Apakah konser ini gratis?", a: "Tiket masuk berupa donasi sukarela mulai Rp25.000, dibayar di gerbang atau lewat rekening donasi di undangan ini." },
      { q: "Boleh membawa anak-anak?", a: "Sangat boleh. Ada area lesehan keluarga di depan panggung dan pojok dongeng sebelum konser." },
      { q: "Bagaimana jika hujan?", a: "Konser tetap berjalan. Area tribun beratap, panitia juga menyiapkan jas hujan." },
    ] },
  },
});
