import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Adrian",
    brideFull: "Kirana Larasati Wibowo, B.A.", groomFull: "Adrian Pradipta Halim, M.Arch.",
    brideParents: "Putri kedua dari\nBapak Hendro Wibowo & Ibu Maria Kristiani", groomParents: "Putra sulung dari\nBapak Johan Halim & Ibu Lily Santoso",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Satu toast untuk kasih yang sabar, dan satu lagi untuk tahun-tahun yang akan datang.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T10:00:00+07:00",
  place: "Gedung Arsip Nasional",
  address: "Jl. Gajah Mada No. 111, Krukut, Taman Sari, Jakarta Barat",
  stories: [
    { date: "2018", title: "Pameran Arsitektur Kota Tua", body: "Kirana memandu tur, Adrian datang terlambat dan terus bertanya tentang lampu gantung tahun 1920-an." },
    { date: "2022", title: "Jarak Jakarta – Rotterdam", body: "Dua tahun studi di Belanda, surat-surat panjang dan panggilan video setiap Minggu pagi." },
    { date: "2026", title: "Lamaran di Rooftop", body: "Di bawah langit Jakarta, dengan sebotol sampanye dan cincin yang disimpan sejak bulan Mei." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-06-19T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gereja Immanuel Jakarta", address: "Jl. Medan Merdeka Timur No. 10, Gambir, Jakarta Pusat" },
    { name: "Resepsi & Toast", date: "2027-06-19T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Gedung Arsip Nasional", address: "Jl. Gajah Mada No. 111, Krukut, Taman Sari, Jakarta Barat" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/r88.webp", "/themes/img/a31.webp", "/themes/img/a77.webp", "/themes/img/a76.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0938 44", account_name: "Kirana Larasati Wibowo" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1270 0098 1123", account_name: "Adrian Pradipta Halim" },
    { id: "demo-kado", type: "address", address: "Jl. Cikini Raya No. 48, Menteng, Jakarta Pusat 10330" },
  ],
  guestName: "Bapak Antonius Gunawan & Partner",
  guestTable: "Meja 7",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati; ia tidak cemburu. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu.", source: "1 Korintus 13:4, 7" },
    rundown: { items: [
      { time: "18.30", title: "Cocktail & welcome drink", note: "Lobi utama" },
      { time: "19.15", title: "Grand entrance & first dance" },
      { time: "19.45", title: "Champagne toast", note: "Menara sampanye" },
      { time: "20.00", title: "Makan malam & jazz" },
    ] },
    dressCode: { note: "Black tie bernuansa 1920-an. Sampanye, gading, dan hitam dipersilakan.", colors: ["#1a1714", "#cdb27e", "#efe0bd", "#f5efe2"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendro Wibowo", "Kel. Besar Bpk. Johan Halim"] },
  },
});
