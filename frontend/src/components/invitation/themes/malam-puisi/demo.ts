import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rara Kinanti", groom: "Bait Senja",
    brideFull: "Kinanti Wulandari Sasmita",
    brideParents: "Penyair tamu, penulis kumpulan puisi \"Kota yang Menunggu Hujan\" (2025)",
    groomFull: "Komunitas Sastra Bait Senja",
    groomParents: "Ruang baca dan panggung puisi kecil di Yogyakarta, sejak 2016",
    note: "Satu panggung kecil, satu mikrofon, dan kursi untuk siapa saja yang membawa kata-kata.",
  },
  eventLabel: "Malam Puisi",
  date: "2027-09-18T19:00:00+07:00",
  place: "Kedai Teater Lampu Kuning",
  address: "Jl. Prawirotaman No. 27, Brontokusuman, Mergangsan, Kota Yogyakarta",
  story: { title: "Susunan Acara", body: "" },
  stories: [
    { date: "19.00", title: "Pembukaan & Musikalisasi Puisi", body: "Petikan gitar akustik dan dua puisi dari pengurus komunitas Bait Senja." },
    { date: "19.30", title: "Panggung Terbuka", body: "Sepuluh pembaca dari pendaftaran di tempat. Lima menit per orang, bawa puisimu sendiri." },
    { date: "20.30", title: "Pembacaan Rara Kinanti", body: "Rara membacakan karya dari kumpulan barunya, diiringi biola dan cahaya lilin." },
    { date: "21.15", title: "Bincang Sastra & Tanda Tangan", body: "Tanya jawab santai seputar proses menulis, dilanjutkan sesi tanda tangan buku." },
  ],
  events: [
    { name: "Pendaftaran Panggung Terbuka", date: "2027-09-18T18:30:00+07:00", time: "18.30 – 19.00 WIB", venue: "Meja depan Kedai Teater Lampu Kuning", address: "Jl. Prawirotaman No. 27, Brontokusuman, Mergangsan, Kota Yogyakarta" },
    { name: "Malam Puisi Vol. 12", date: "2027-09-18T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Panggung Kedai Teater Lampu Kuning", address: "Jl. Prawirotaman No. 27, Brontokusuman, Mergangsan, Kota Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-donasi", type: "bank", bank_name: "BNI", account_number: "0845 2210 93", account_name: "Komunitas Sastra Bait Senja" },
  ],
  guestName: "Sdri. Anindya Putri",
  guestTable: "Kursi Baris 2",
  extras: {
    quote: { text: "Kita datang membawa sunyi masing-masing, dan pulang membawa suara orang lain yang tiba-tiba terasa seperti milik sendiri.", source: "Bait Senja" },
    dressCode: { note: "Bebas dan nyaman. Kalau ingin ikut suasana: cokelat kayu, marun, dan krem.", colors: ["#2b1a14", "#6e1620", "#c99a45", "#f3e6c9"] },
    guestPass: { note: "Tunjukkan kode ini di meja depan untuk mendapat kursi dan pembatas buku edisi malam ini." },
    rsvpDietary: {},
    faq: { items: [
      { q: "Apakah acara ini gratis?", a: "Gratis dan terbuka untuk umum. Donasi sukarela untuk perpustakaan jalanan komunitas diterima di meja depan." },
      { q: "Bagaimana cara ikut membaca puisi?", a: "Daftar di meja depan pukul 18.30. Kuota sepuluh pembaca, masing-masing lima menit." },
      { q: "Boleh membawa puisi karya orang lain?", a: "Panggung terbuka khusus untuk karya sendiri. Silakan bawa tulisanmu, sependek apa pun." },
    ] },
  },
});
