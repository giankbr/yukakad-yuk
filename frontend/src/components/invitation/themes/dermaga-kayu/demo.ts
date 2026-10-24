import { makeDemo } from "../demo-base";

// Pernikahan di tepi pantai Belitung saat matahari terbit: janji suci di ujung dermaga kayu, resepsi di paviliun pantai.
export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Dimas",
    brideFull: "Alya Prameswari Hutomo", groomFull: "Dimas Arya Wicaksana",
    brideParents: "Putri dari\nBapak Hendra Hutomo & Ibu Maria Lestiani", groomParents: "Putra dari\nBapak Bambang Wicaksana & Ibu Ratna Dewi",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Kami memilih pagi yang tenang dan dermaga yang panjang, karena perjalanan terbaik dimulai pelan-pelan, bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T06:30:00+07:00",
  place: "Dermaga Tanjung Kelayang",
  address: "Pantai Tanjung Kelayang, Keciput, Sijuk, Kabupaten Belitung",
  stories: [
    { date: "2021", title: "Kapal yang Sama", body: "Duduk bersebelahan di kapal penyeberangan menuju Pulau Lengkuas, dan mengobrol sampai lupa memotret mercusuar." },
    { date: "2024", title: "Pagi-pagi di Pantai", body: "Kebiasaan kecil kami: mengejar matahari terbit di pantai mana pun, membawa termos teh dan roti bakar." },
    { date: "2026", title: "Di Ujung Dermaga", body: "Dimas melamar tepat saat matahari menyentuh laut. Alya menjawab sebelum mataharinya naik sepenuhnya." },
  ],
  events: [
    { name: "Janji Suci di Dermaga", date: "2027-09-25T06:30:00+07:00", time: "06.30 – 07.30 WIB", venue: "Dermaga Tanjung Kelayang", address: "Pantai Tanjung Kelayang, Keciput, Sijuk, Kabupaten Belitung" },
    { name: "Sarapan & Resepsi Pantai", date: "2027-09-25T08:30:00+07:00", time: "08.30 – 12.00 WIB", venue: "Paviliun Pasir Putih", address: "Jl. Tanjung Kelayang No. 8, Keciput, Sijuk, Kabupaten Belitung" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/a21.webp", "/themes/img/r107.webp", "/themes/img/r106.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1640 0098 1123", account_name: "Alya Prameswari Hutomo" },
    { id: "demo-kado", type: "address", address: "Jl. Sriwijaya No. 41, Tanjung Pendam, Tanjung Pandan, Belitung 33411" },
  ],
  guestName: "Bapak Yohanes Gunawan & Keluarga",
  guestTable: "Meja Kerang 4",
  extras: {
    quote: { text: "Cinta tidak saling menatap, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "06.15", title: "Tamu berkumpul di pangkal dermaga", note: "Disediakan sandal pantai" },
      { time: "06.30", title: "Janji suci saat matahari terbit" },
      { time: "08.30", title: "Sarapan bersama di paviliun" },
      { time: "10.00", title: "Foto bersama di dermaga" },
    ] },
    dressCode: { note: "Busana pantai yang santai dan rapi. Warna lilac, peach, krem, atau biru laut.", colors: ["#c7b6d8", "#f4c3a4", "#f3e6d4", "#8fb3c4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Hendra Hutomo", "Kel. Besar Bambang Wicaksana"] },
    travel: { note: "Untuk tamu dari luar Belitung, berikut pilihan terdekat dari lokasi.", items: [
      { name: "Bandara H.A.S. Hanandjoeddin", detail: "± 45 menit berkendara ke Tanjung Kelayang" },
      { name: "Penginapan tepi pantai", detail: "Beberapa resor dalam radius 1 km dari dermaga" },
    ] },
    faq: { items: [
      { q: "Kenapa acaranya sepagi itu?", a: "Agar kita menyaksikan matahari terbit bersama. Mohon tiba pukul 06.15 WIB." },
      { q: "Bagaimana jika cuaca buruk?", a: "Janji suci dipindahkan ke Paviliun Pasir Putih, beberapa langkah dari dermaga." },
    ] },
  },
});
