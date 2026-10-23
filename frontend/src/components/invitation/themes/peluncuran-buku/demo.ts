import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinanti Larasati", groom: "Teras Aksara",
    brideFull: "Kinanti Larasati", groomFull: "Penerbit Teras Aksara",
    brideParents: "Penulis novel \"Rumah di Ujung Musim\".\nLahir di Magelang, kini menulis dan mengajar di Yogyakarta.",
    groomParents: "Penerbit independen di Yogyakarta sejak 2014,\nrumah bagi fiksi dan esai penulis muda.",
    bridePhoto: "/themes/img/r53.webp",
    note: "Sebuah novel tentang tiga generasi perempuan, satu rumah kayu di lereng Merapi, dan musim-musim yang datang tanpa permisi.",
  },
  eventLabel: "Peluncuran Buku",
  date: "2027-03-13T15:00:00+07:00",
  place: "Ruang Baca Kotabaru",
  address: "Jl. Faridan M. Noto No. 12, Kotabaru, Gondokusuman, Yogyakarta",
  story: { title: "Perjalanan Buku", body: "" },
  stories: [
    { date: "Januari 2022", title: "Halaman Pertama", body: "Bab pertama ditulis tangan di buku catatan bersampul cokelat, di beranda rumah nenek saat hujan turun seharian." },
    { date: "Agustus 2025", title: "Naskah Diterima", body: "Setelah tujuh kali revisi, naskah diterima Teras Aksara dan mulai disunting bersama editor Rani Pramesti." },
    { date: "Maret 2027", title: "Cetakan Pertama", body: "Tiga ribu eksemplar cetakan pertama tiba di gudang, masih harum tinta, siap bertemu pembacanya." },
  ],
  events: [
    { name: "Peluncuran & Diskusi Buku", date: "2027-03-13T15:00:00+07:00", time: "15.00 – 17.00 WIB", venue: "Ruang Baca Kotabaru", address: "Jl. Faridan M. Noto No. 12, Kotabaru, Gondokusuman, Yogyakarta" },
    { name: "Sesi Tanda Tangan & Ramah Tamah", date: "2027-03-13T17:00:00+07:00", time: "17.00 – 18.00 WIB", venue: "Teras Ruang Baca Kotabaru", address: "Jl. Faridan M. Noto No. 12, Kotabaru, Gondokusuman, Yogyakarta" },
  ],
  gallery: ["/themes/img/r54.webp", "/themes/img/r53.webp", "/themes/img/a114.webp", "/themes/img/r100.webp"],
  gifts: [
    { id: "demo-po", type: "bank", bank_name: "BNI", account_number: "0398 1172 46", account_name: "Teras Aksara (Pre-order)" },
    { id: "demo-donasi", type: "address", address: "Taman Baca Lereng Merapi, Dusun Kaliurang Barat, Hargobinangun, Pakem, Sleman 55582" },
  ],
  guestName: "Sdr. Arya Nugraha",
  guestTable: "Kursi Baris B",
  extras: {
    quote: { text: "Rumah bukan tempat kita pulang, melainkan orang-orang yang menunggu kita membuka pintu.", source: "Rumah di Ujung Musim, hlm. 212" },
    rundown: { items: [
      { time: "15.00", title: "Registrasi & teh sore" },
      { time: "15.30", title: "Pembacaan petikan novel", note: "Dibacakan oleh penulis" },
      { time: "15.50", title: "Diskusi buku", note: "Moderator: Bayu Wicaksono, kritikus sastra" },
      { time: "16.40", title: "Tanya jawab pembaca" },
      { time: "17.00", title: "Tanda tangan & foto bersama" },
    ] },
    faq: { items: [
      { q: "Apakah acara ini gratis?", a: "Gratis dan terbuka untuk umum. Mohon konfirmasi kehadiran agar kami bisa menyiapkan kursi." },
      { q: "Bisakah membeli buku di lokasi?", a: "Bisa. Tersedia edisi bertanda tangan dengan harga khusus peluncuran Rp98.000." },
      { q: "Bolehkah membawa buku untuk didonasikan?", a: "Sangat boleh. Kotak donasi untuk Taman Baca Lereng Merapi ada di meja registrasi." },
    ] },
    guestPass: {},
  },
});
