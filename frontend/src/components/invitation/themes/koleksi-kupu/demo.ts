import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Renata", groom: "Gilang",
    brideFull: "Renata Kusumawardhani, M.Si.", groomFull: "Gilang Prasetya Nugraha, S.Hut.",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    brideParents: "Putri kedua dari\nBapak Ir. Handoko Wibisono & Ibu Retno Palupi", groomParents: "Putra sulung dari\nBapak Agus Nugraha & Ibu Lestari Wulandari",
    note: "Dua pengamat yang sama-sama sabar menunggu sesuatu yang indah hinggap. Kali ini, kami yang memutuskan untuk tinggal.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T10:00:00+07:00",
  place: "Gedung Arsip Lama",
  address: "Jl. Ir. H. Juanda No. 9, Paledang, Bogor Tengah, Kota Bogor",
  story: { title: "Catatan Lapangan", body: "" },
  stories: [
    { date: "Juli 2019", title: "Lembah Bantimurung", body: "Dua relawan survei kupu-kupu tersesat di jalur yang sama. Renata mencatat, Gilang memotret, dan kami pulang dengan satu buku catatan berdua." },
    { date: "2021 – 2025", title: "Spesimen yang Bertambah", body: "Dari Kebun Raya Bogor sampai hutan Halimun, kami menulis label demi label sambil belajar saling memahami." },
    { date: "Januari 2027", title: "Sebuah Kotak Kaca", body: "Gilang melamar dengan kotak koleksi kecil berisi satu label tulisan tangan: maukah kamu menjadi pasangan seumur hidupku?" },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-06-12T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gedung Arsip Lama", address: "Jl. Ir. H. Juanda No. 9, Paledang, Bogor Tengah, Kota Bogor" },
    { name: "Resepsi di Taman", date: "2027-06-12T16:00:00+07:00", time: "16.00 – 19.00 WIB", venue: "Taman Belakang Gedung Arsip Lama", address: "Jl. Ir. H. Juanda No. 9, Paledang, Bogor Tengah, Kota Bogor" },
  ],
  gallery: ["/themes/img/r44.webp", "/themes/img/r97.webp", "/themes/img/r55.webp", "/themes/img/r43.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0613 2207 19", account_name: "Renata Kusumawardhani" },
    { id: "demo-kado", type: "address", address: "Jl. Pangrango No. 21, Babakan, Bogor Tengah, Kota Bogor 16128" },
  ],
  guestName: "Bapak Yohanes Sudarmadi & Keluarga",
  guestTable: "Lemari 4",
  extras: {
    quote: { text: "Kupu-kupu tidak menghitung bulan, melainkan saat-saat, dan ia selalu punya cukup waktu.", source: "Rabindranath Tagore" },
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Keluarga & sahabat dekat" },
      { time: "11.30", title: "Ramah tamah & foto keluarga" },
      { time: "16.00", title: "Resepsi taman dibuka", note: "Tur singkat ruang koleksi" },
      { time: "18.00", title: "Dansa pertama & potong kue" },
    ] },
    dressCode: { note: "Nuansa museum tua: hijau botol, cokelat kenari, krem linen, dan sentuhan kuning kunyit.", colors: ["#2c3a31", "#5a3a24", "#ece3cf", "#d9a23a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ir. Handoko Wibisono", "Kel. Besar Agus Nugraha"] },
  },
});
