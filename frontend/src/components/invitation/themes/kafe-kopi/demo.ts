import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinan", groom: "Bram",
    brideFull: "Kinanti Ayuningtyas", groomFull: "Bramantyo Adi Nugroho",
    brideParents: "Putri dari Bapak Sutrisno Wibowo\n& Ibu Endah Kusumawati", groomParents: "Putra dari Bapak Yohanes Nugroho\n& Ibu Maria Sri Lestari",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Satu cangkir untuk berdua: pahitnya kami bagi, manisnya kami nikmati pelan-pelan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-13T10:00:00+07:00",
  place: "Rumah Kopi Kalijaga",
  address: "Jl. Prawirotaman No. 18, Brontokusuman, Mergangsan, Kota Yogyakarta",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Agustus 2020", title: "Pesanan yang Tertukar", body: "Kinan memesan cappuccino, Bram memesan kopi tubruk. Barista menukar keduanya, dan kami malah mengobrol sampai kafe tutup." },
    { date: "2022", title: "Meja Pojok Dekat Jendela", body: "Setiap Sabtu pagi kami duduk di meja yang sama. Kinan menulis, Bram menggambar, dua cangkir selalu habis duluan." },
    { date: "Maret 2027", title: "Latte Art Berbentuk Hati", body: "Bram belajar latte art berbulan-bulan hanya untuk satu cangkir. Di busanya tertulis pertanyaan, dan Kinan menjawab ya." },
    { date: "November 2027", title: "Cangkir untuk Berdua", body: "Kami merayakan hari bahagia di kafe tempat semuanya dimulai, ditemani aroma kopi, keluarga, dan sahabat." },
  ],
  events: [
    { name: "Ikrar Janji", date: "2027-11-13T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Ruang Jendela, Rumah Kopi Kalijaga", address: "Jl. Prawirotaman No. 18, Brontokusuman, Mergangsan, Kota Yogyakarta" },
    { name: "Resepsi Kopi Sore", date: "2027-11-13T15:00:00+07:00", time: "15.00 – 18.00 WIB", venue: "Taman Belakang, Rumah Kopi Kalijaga", address: "Jl. Prawirotaman No. 18, Brontokusuman, Mergangsan, Kota Yogyakarta" },
  ],
  gallery: ["/themes/img/r72.webp", "/themes/img/a132.webp", "/themes/img/r73.webp", "/themes/img/r6.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0029 0110 4552 507", account_name: "Kinanti Ayuningtyas" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0819 0433 2716", account_name: "Bramantyo Adi Nugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Tirtodipuran No. 7, Mantrijeron, Kota Yogyakarta 55143" },
  ],
  guestName: "Mas Galih & Partner",
  guestTable: "Meja Jendela 2",
  extras: {
    rundown: { items: [
      { time: "15.00", title: "Welcome drink: es kopi susu gula aren" },
      { time: "15.30", title: "Sambutan dan cerita singkat kami" },
      { time: "16.00", title: "Makan sore & kue-kue tradisional" },
      { time: "17.00", title: "Kelas latte art kilat bersama barista" },
    ] },
    dressCode: { note: "Santai rapi dengan warna kopi: cokelat, krem, terakota, dan hijau daun. Tidak ada aturan ketat, yang penting nyaman.", colors: ["#4a2c1c", "#e8c9a0", "#c4673f", "#5d7a4f"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Sutrisno Wibowo", "Keluarga Besar Yohanes Nugroho"] },
    faq: { items: [
      { q: "Apakah tersedia minuman non-kopi?", a: "Tentu. Ada teh rempah, cokelat panas, dan jus segar untuk yang tidak minum kopi." },
      { q: "Di mana tempat parkir?", a: "Parkir mobil di Jl. Prawirotaman sisi utara, sekitar 2 menit berjalan kaki. Motor bisa parkir di halaman kafe." },
    ] },
  },
});
