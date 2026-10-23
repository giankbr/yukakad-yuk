import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Elvan",
    brideFull: "Kirana Anindya Wijaya", groomFull: "Elvan Pradipta Hartanto, M.Sc.",
    brideParents: "Putri tunggal dari\nBapak Hendra Wijaya & Ibu Maria Lestari", groomParents: "Putra kedua dari\nBapak Yohanes Hartanto & Ibu Sri Rejeki",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Kami bertemu di musim yang paling dingin, dan sejak itu tidak pernah merasa kedinginan lagi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-12-18T16:00:00+07:00",
  place: "Paviliun Kaca, Villa Kabut Lembang",
  address: "Jl. Raya Tangkuban Parahu Km. 9, Cikole, Lembang, Kabupaten Bandung Barat",
  stories: [
    { date: "Januari 2021", title: "Salju Pertama", body: "Dua mahasiswa Indonesia di Sapporo terjebak badai salju di halte yang sama. Satu termos teh jahe dibagi berdua." },
    { date: "2023", title: "Pulang Bersama", body: "Lulus di musim semi, kembali ke Bandung, dan tetap berkabar setiap kali kabut Lembang turun." },
    { date: "Desember 2026", title: "Lamaran", body: "Di depan jendela berembun, Elvan bertanya dengan suara gemetar. Kirana menjawab sebelum pertanyaannya selesai." },
    { date: "Desember 2027", title: "Hari Kami", body: "Kami memilih bulan paling sejuk untuk mengikat janji, ditemani keluarga dan sahabat terdekat." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-12-18T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Paviliun Kaca, Villa Kabut Lembang", address: "Jl. Raya Tangkuban Parahu Km. 9, Cikole, Lembang, Kabupaten Bandung Barat" },
    { name: "Resepsi Malam", date: "2027-12-18T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Aula Pinus, Villa Kabut Lembang", address: "Jl. Raya Tangkuban Parahu Km. 9, Cikole, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/a77.webp", "/themes/img/r88.webp", "/themes/img/a76.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "8015 3329 40", account_name: "Kirana Anindya Wijaya" },
    { id: "demo-kado", type: "address", address: "Jl. Setiabudhi No. 182, Hegarmanah, Cidadap, Kota Bandung 40141" },
  ],
  guestName: "Bapak Stefanus Gunadi & Partner",
  guestTable: "Meja Edelweis 4",
  extras: {
    quote: { text: "Mencintai bukanlah saling menatap, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "16.00", title: "Upacara pernikahan", note: "Paviliun kaca menghadap kebun pinus" },
      { time: "17.15", title: "Teh hangat & foto bersama" },
      { time: "18.30", title: "Resepsi malam dibuka", note: "Makan malam & musik akustik" },
    ] },
    dressCode: { note: "Formal hangat. Udara Lembang sejuk di malam hari, silakan membawa jas atau selendang. Nuansa putih, perak, dan biru es.", colors: ["#f3f7fa", "#b8c9d9", "#5f7d9c", "#23405e"] },
    guestPass: {},
    rsvpDietary: {},
    travel: { note: "Untuk tamu dari luar kota:", items: [
      { name: "Shuttle dari Bandung", detail: "Berangkat 14.30 WIB dari Jl. Setiabudhi No. 182" },
      { name: "Parkir", detail: "Area parkir villa, dipandu petugas" },
    ] },
    family: { names: ["Kel. Besar Hendra Wijaya", "Kel. Besar Yohanes Hartanto"] },
  },
});
