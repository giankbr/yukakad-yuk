import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Galih",
    brideFull: "Maria Ayu Kinanti, S.Si.", groomFull: "Yohanes Galih Pramudya, M.Sc.",
    brideParents: "Putri sulung dari\nBapak Fransiskus Hadi Santoso & Ibu Bernadetta Sri Lestari", groomParents: "Putra ketiga dari\nBapak Antonius Pramono & Ibu Theresia Wahyuni",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Dikumpulkan dengan sabar, dikeringkan oleh waktu, disimpan untuk selamanya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T10:00:00+07:00",
  place: "Kebun Raya Bogor",
  address: "Jl. Ir. H. Juanda No. 13, Paledang, Bogor Tengah, Kota Bogor",
  stories: [
    { date: "12 Mei 2019", title: "Spesimen pertama", body: "Bertemu di ruang herbarium kampus. Ayu salah mengambil map spesimen pakis milik Galih, dan kami tertawa karena label tulisan tangannya sama-sama berantakan." },
    { date: "2022", title: "Ekspedisi Gunung Gede", body: "Mendaki bersama untuk mendata anggrek liar. Di pos terakhir, Galih menyelipkan bunga edelweis kering di buku catatan Ayu." },
    { date: "2026", title: "Lamaran di rumah kaca", body: "Di antara rak-rak tanaman, dengan cincin yang disembunyikan di dalam kotak biji." },
  ],
  events: [
    { name: "Misa Pemberkatan", date: "2027-08-14T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gereja Katedral Bogor", address: "Jl. Kapten Muslihat No. 22, Paledang, Bogor Tengah, Kota Bogor" },
    { name: "Resepsi Taman", date: "2027-08-14T16:00:00+07:00", time: "16.00 – 19.00 WIB", venue: "Kebun Raya Bogor", address: "Jl. Ir. H. Juanda No. 13, Paledang, Bogor Tengah, Kota Bogor" },
  ],
  gallery: ["/themes/img/r1.webp", "/themes/img/r27.webp", "/themes/img/r16.webp", "/themes/img/r29.webp", "/themes/img/a18.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0953 4412 78", account_name: "Maria Ayu Kinanti" },
    { id: "demo-kado", type: "address", address: "Jl. Pangrango No. 7, Babakan, Bogor Tengah, Kota Bogor 16128" },
  ],
  guestName: "Bapak Dr. Stefanus Wirawan & Keluarga",
  guestTable: "Meja 12",
  extras: {
    quote: { text: "Di ladang telah tampak bunga-bunga, tibalah musim memangkas; bunyi tekukur terdengar di tanah kita.", source: "Kidung Agung 2:12" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu", note: "Taman Teijsmann" },
      { time: "16.45", title: "Prosesi masuk pengantin" },
      { time: "17.15", title: "Makan malam di taman" },
      { time: "18.30", title: "Lagu & foto bersama" },
    ] },
    dressCode: { note: "Garden formal. Warna tanah, krem, hijau zaitun, dan mauve dipersilakan.", colors: ["#b68e60", "#f1e9d6", "#98955f", "#c88aa4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Fransiskus Hadi Santoso", "Kel. Besar Bpk. Antonius Pramono"] },
  },
});
