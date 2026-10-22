import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Raka",
    brideFull: "Nadia Rahmawati",
    groomFull: "Raka Adi Pratama",
    brideParents: "Pendiri, peracik menu, dan penjaga resep kue rumahan Senja",
    groomParents: "Kepala barista dan penyangrai biji kopi Nusantara",
    bridePhoto: "/themes/img/r3.webp",
    groomPhoto: "/themes/img/r4.webp",
    note: "Dari gerobak kopi kecil di hari Minggu, kini kami punya rumah sendiri. Datang, cicipi, dan rayakan awal yang baru bersama kami.",
  },
  eventLabel: "Grand Opening",
  date: "2027-07-10T15:00:00+07:00",
  place: "Kedai Kopi Senja",
  address: "Jl. Soekarno Hatta No. 27, Lowokwaru, Kota Malang, Jawa Timur",
  story: { title: "Cerita Kedai Kopi Senja", body: "" },
  stories: [
    { date: "2023", title: "Gerobak di hari Minggu", body: "Semua berawal dari gerobak kopi kecil di area hari bebas kendaraan, dua termos, dan satu resep kopi susu gula aren." },
    { date: "2025", title: "Belajar menyangrai", body: "Raka mulai menyangrai biji kopi dari petani di lereng Arjuno, Nadia menyempurnakan resep kue pendamping." },
    { date: "2026", title: "Ruko di sudut jalan", body: "Kami menemukan ruko mungil dengan jendela besar yang menghadap matahari terbenam, tempat yang pas untuk sebuah kedai bernama Senja." },
    { date: "2027", title: "Pintu dibuka", body: "Setelah berbulan-bulan merenovasi bersama keluarga dan sahabat, kedai siap menyambut tamu pertamanya." },
  ],
  events: [
    { name: "Pengguntingan Pita & Doa Bersama", date: "2027-07-10T15:00:00+07:00", time: "15.00 – 15.30 WIB", venue: "Kedai Kopi Senja", address: "Jl. Soekarno Hatta No. 27, Lowokwaru, Kota Malang, Jawa Timur" },
    { name: "Open House & Cicip Menu Perdana", date: "2027-07-10T15:30:00+07:00", time: "15.30 – 21.00 WIB", venue: "Kedai Kopi Senja", address: "Jl. Soekarno Hatta No. 27, Lowokwaru, Kota Malang, Jawa Timur" },
  ],
  gallery: ["/themes/img/r25.webp"],
  gifts: [],
  guestName: "Bapak Yudhistira & Rekan",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "15.00", title: "Sambutan pemilik & doa bersama" },
      { time: "15.15", title: "Pengguntingan pita", note: "Tamu dipersilakan berkumpul di depan pintu" },
      { time: "15.30", title: "Cicip menu perdana gratis", note: "Kopi susu gula aren, teh rempah, dan kue rumahan" },
      { time: "19.00", title: "Musik akustik di teras", note: "Bersama teman-teman musisi Malang" },
    ] },
    guestPass: {},
    family: { title: "Turut mengundang", names: ["Keluarga Besar Rahmawati", "Keluarga Besar Pratama", "Tim Kedai Kopi Senja"] },
    faq: { items: [
      { q: "Apakah ada promo di hari pembukaan?", a: "Ada! Setiap tamu mendapat satu minuman gratis dan kartu stempel dengan bonus dua stempel." },
      { q: "Di mana tempat parkir?", a: "Parkir motor di depan kedai, parkir mobil di halaman ruko sebelah yang sudah kami sewa khusus hari ini." },
    ] },
  },
});
