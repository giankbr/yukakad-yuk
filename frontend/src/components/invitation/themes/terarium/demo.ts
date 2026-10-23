import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anindya", groom: "Bastian",
    brideFull: "Anindya Maharani Putri", groomFull: "Bastian Wirawan Hadiprana",
    brideParents: "Putri dari Bapak Hendro Santoso\n& Ibu Maria Kristiani", groomParents: "Putra dari Bapak Yosef Hadiprana\n& Ibu Lusiana Wirawan",
    bridePhoto: "/themes/img/a97.webp", groomPhoto: "/themes/img/a96.webp",
    note: "Cinta seperti taman kecil di dalam kaca: cukup cahaya, sedikit air setiap hari, dan kesabaran untuk melihatnya tumbuh.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T10:00:00+07:00",
  place: "Rumah Kaca Lembang",
  address: "Jl. Kolonel Masturi No. 215, Cikole, Lembang, Kabupaten Bandung Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Lokakarya Terarium", body: "Kami duduk bersebelahan di kelas membuat terarium. Bastian menumpahkan pasir, Anindya menolong menata lumutnya." },
    { date: "2023", title: "Satu Rak, Dua Pemilik", body: "Rak di kamar Anindya mulai penuh dengan terarium buatan berdua. Setiap toples punya nama dan cerita." },
    { date: "Des 2026", title: "Di Dalam Toples", body: "Bastian menyembunyikan cincin di bawah batu putih sebuah terarium kecil. Anindya baru menemukannya setelah tiga hari." },
    { date: "Mei 2027", title: "Tumbuh Bersama", body: "Kami mengikat janji di rumah kaca, dikelilingi pakis dan sukulen, bersama keluarga dan sahabat." },
  ],
  events: [
    { name: "Ikrar Janji", date: "2027-05-15T10:00:00+07:00", time: "10.00 – 11.00 WIB", venue: "Rumah Kaca Lembang", address: "Jl. Kolonel Masturi No. 215, Cikole, Lembang, Kabupaten Bandung Barat" },
    { name: "Resepsi Taman", date: "2027-05-15T12:00:00+07:00", time: "12.00 – 15.00 WIB", venue: "Taman Pakis, Rumah Kaca Lembang", address: "Jl. Kolonel Masturi No. 215, Cikole, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/a26.webp", "/themes/img/a123.webp", "/themes/img/r84.webp", "/themes/img/r93.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2830 5150 27", account_name: "Anindya Maharani Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Bukit Pakar Timur No. 9, Ciburial, Cimenyan, Kabupaten Bandung 40198" },
  ],
  guestName: "Ibu Theresia Wulandari & Keluarga",
  guestTable: "Meja Pakis 4",
  extras: {
    rundown: { items: [
      { time: "12.00", title: "Sambutan & minuman jahe sereh" },
      { time: "12.30", title: "Makan siang di bawah atap kaca" },
      { time: "13.30", title: "Tamu membuat terarium mini untuk dibawa pulang" },
      { time: "14.30", title: "Potong kue & foto bersama" },
    ] },
    dressCode: { note: "Santai rapi bernuansa taman. Hijau lumut, krem, dan terakota dipersilakan. Hindari hak tinggi yang tipis karena area berumput.", colors: ["#2f5a3f", "#a7bd64", "#e9e3d3", "#c27a5a"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Hendro Santoso", "Keluarga Besar Yosef Hadiprana"] },
    faq: { items: [
      { q: "Apakah acara di dalam ruangan?", a: "Ikrar janji di dalam rumah kaca, resepsi di taman beratap kanopi. Udara Lembang sejuk, bawalah jaket tipis." },
      { q: "Bolehkah membawa anak?", a: "Tentu. Ada meja kecil untuk anak-anak membuat terarium bersama pendamping." },
    ] },
  },
});
