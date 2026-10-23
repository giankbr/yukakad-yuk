import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Bastian",
    brideFull: "Kirana Ayu Wulandari", groomFull: "Bastian Arya Pratama",
    brideParents: "Putri dari\nBapak Hendro Wibisono & Ibu Ratna Kusumawati",
    groomParents: "Putra dari\nBapak Yohanes Setiawan & Ibu Maria Lestari",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Pagi berkabut, kopi hangat di dermaga, dan satu janji sederhana: pulang ke rumah yang sama setiap hari.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-24T09:00:00+07:00",
  place: "Kabin Telaga Pinus",
  address: "Kawasan Situ Patenggang, Patengan, Rancabali, Kabupaten Bandung, Jawa Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Tersesat di Jalur Pendakian", body: "Kami bertemu di pos dua sebuah jalur pendakian yang berkabut. Bastian membawa peta, Kirana membawa termos teh. Peta ternyata salah, tehnya yang menyelamatkan hari itu." },
    { date: "2022", title: "Kano Pertama", body: "Bastian mengajak Kirana belajar mendayung kano di danau. Kanonya terbalik dua kali, tetapi kami tertawa sepanjang sore." },
    { date: "2026", title: "Di Ujung Dermaga", body: "Di dermaga kayu pada pagi yang dingin, dengan lentera yang masih menyala, Bastian bertanya. Kirana menjawab sebelum pertanyaannya selesai." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-07-24T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Dermaga Kabin Telaga Pinus", address: "Kawasan Situ Patenggang, Patengan, Rancabali, Kabupaten Bandung" },
    { name: "Makan Siang Tepi Danau", date: "2027-07-24T11:30:00+07:00", time: "11.30 – 15.00 WIB", venue: "Paviliun Kayu Telaga Pinus", address: "Kawasan Situ Patenggang, Patengan, Rancabali, Kabupaten Bandung" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/r89.webp", "/themes/img/r92.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4380 7719 02", account_name: "Kirana Ayu Wulandari" },
    { id: "demo-jago", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 2245 7731", account_name: "Bastian Arya Pratama" },
    { id: "demo-alamat", type: "address", address: "Jl. Cigadung Raya Timur No. 14, Cibeunying Kaler, Bandung 40191" },
  ],
  guestName: "Kak Dimas & Partner",
  guestTable: "Meja Cemara",
  extras: {
    quote: { text: "Rumah bukanlah sebuah tempat, melainkan seseorang yang selalu membuatmu ingin pulang.", source: "Kirana & Bastian" },
    rundown: { items: [
      { time: "08.30", title: "Kedatangan tamu", note: "Teh jahe & kopi hangat di beranda kabin" },
      { time: "09.00", title: "Upacara pernikahan", note: "Di ujung dermaga" },
      { time: "10.30", title: "Foto bersama", note: "Saat kabut mulai naik" },
      { time: "11.30", title: "Makan siang tepi danau" },
    ] },
    dressCode: { note: "Hangat dan santai: rajut, flanel, atau linen. Danau dingin di pagi hari, bawa jaket tipis dan sepatu yang nyaman.", colors: ["#29463b", "#b2452e", "#e8d9c2", "#7d97a0"] },
    guestPass: {},
    rsvpDietary: {},
    travel: { note: "Lokasi sekitar dua jam dari pusat Kota Bandung.", items: [
      { name: "Shuttle tamu", detail: "Berangkat 06.30 dari Jl. Dago, kursi terbatas" },
      { name: "Penginapan sekitar danau", detail: "Kabin dan glamping, kode promo KIRANABASTIAN" },
    ] },
    faq: { items: [
      { q: "Apakah acaranya di luar ruangan?", a: "Ya, upacara di dermaga dan makan siang di paviliun beratap. Jika hujan, semua pindah ke paviliun." },
      { q: "Boleh membawa anak?", a: "Tentu. Mohon diawasi saat di dermaga, pelampung anak tersedia." },
    ] },
  },
});
