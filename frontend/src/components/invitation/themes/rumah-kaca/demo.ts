import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Larasati", groom: "Adrian",
    brideFull: "Larasati Wening Prameswari", groomFull: "Adrian Pramudya Santosa",
    brideParents: "Putri dari Bapak Haryo Wibisono\n& Ibu Ratna Kusumastuti", groomParents: "Putra dari Bapak Gunawan Santosa\n& Ibu Elisabeth Rahayu",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Seperti rumah kaca di pagi hari: terang, hangat, dan memberi ruang bagi segala yang ingin tumbuh.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T09:00:00+07:00",
  place: "Griya Kaca Botanika",
  address: "Jl. Ir. H. Juanda No. 22, Paledang, Bogor Tengah, Kota Bogor, Jawa Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Maret 2020", title: "Di Bawah Atap Kaca", body: "Hujan turun deras di kebun raya. Kami berteduh di rumah kaca yang sama, di antara palem dan pakis, lalu mengobrol sampai hujan reda." },
    { date: "2022", title: "Kebun di Balkon", body: "Adrian membawakan sebatang pakis Boston. Dua tahun kemudian balkon Larasati penuh tanaman gantung yang kami rawat bergantian." },
    { date: "Januari 2027", title: "Pagi yang Terang", body: "Di rumah kaca tempat kami pertama bertemu, saat cahaya pagi masuk lewat atap, Adrian bertanya, dan Larasati mengangguk." },
    { date: "Juni 2027", title: "Tumbuh Bersama", body: "Kami mengikat janji di bawah kubah kaca, dikelilingi keluarga, sahabat, dan tanaman yang menjadi saksi kisah kami." },
  ],
  events: [
    { name: "Pemberkatan & Ikrar Janji", date: "2027-06-12T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Paviliun Kubah, Griya Kaca Botanika", address: "Jl. Ir. H. Juanda No. 22, Paledang, Bogor Tengah, Kota Bogor" },
    { name: "Resepsi Pagi", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Sayap Palem, Griya Kaca Botanika", address: "Jl. Ir. H. Juanda No. 22, Paledang, Bogor Tengah, Kota Bogor" },
  ],
  gallery: ["/themes/img/r1.webp", "/themes/img/r84.webp", "/themes/img/a26.webp", "/themes/img/a116.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0953 2210 87", account_name: "Larasati Wening Prameswari" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1330 0175 4429", account_name: "Adrian Pramudya Santosa" },
    { id: "demo-kado", type: "address", address: "Jl. Pakuan Indah No. 14, Tegallega, Bogor Tengah, Kota Bogor 16129" },
  ],
  guestName: "Bapak Hendra Wijaya & Keluarga",
  guestTable: "Meja Palem 3",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu & teh serai hangat" },
      { time: "11.30", title: "Kata sambutan keluarga" },
      { time: "12.00", title: "Santap siang di antara palem" },
      { time: "13.15", title: "Potong kue & foto bersama di bawah kubah" },
    ] },
    dressCode: { note: "Formal santai bernuansa taman pagi: hijau zaitun, krem, dan putih gading. Sepatu berhak lebar lebih nyaman di lantai batu.", colors: ["#2f4a42", "#83b063", "#efe9d8", "#b9764f"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Haryo Wibisono", "Keluarga Besar Gunawan Santosa"] },
    faq: { items: [
      { q: "Apakah acaranya di dalam ruangan?", a: "Ya, seluruh acara di dalam rumah kaca yang sejuk berkat ventilasi atap. Udara Bogor bisa lembap, bawalah kipas kecil." },
      { q: "Di mana tempat parkir?", a: "Parkir tersedia di gerbang timur. Dari sana ada petunjuk jalan setapak menuju Griya Kaca, sekitar 3 menit berjalan kaki." },
    ] },
  },
});
