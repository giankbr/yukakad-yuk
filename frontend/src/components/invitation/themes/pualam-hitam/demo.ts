import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Hamzah",
    brideFull: "Nadia Khairunnisa Harahap, S.Ars.", groomFull: "Hamzah Al-Fatih Wibisono, S.T.",
    brideParents: "Putri tunggal dari\nBapak Ir. H. Taufik Harahap & Ibu Hj. Sarah Lubis", groomParents: "Putra ketiga dari\nBapak H. Bambang Wibisono & Ibu Hj. Dewi Kartika",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Dalam tenang kami bersandar, dalam syukur kami melangkah. Semoga Allah meridhai langkah ini.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-11T09:00:00+07:00",
  place: "The Dharmawangsa Jakarta",
  address: "Jl. Brawijaya Raya No. 26, Pulo, Kebayoran Baru, Jakarta Selatan",
  stories: [
    { date: "2020", title: "Satu Studio", body: "Kami bertemu saat merancang interior sebuah masjid kecil di Depok: Nadia memilih batu, Hamzah menghitung strukturnya." },
    { date: "2026", title: "Lamaran", body: "Di hadapan kedua keluarga, Hamzah menyampaikan niat baiknya. Alhamdulillah, dijawab dengan senyum dan restu." },
    { date: "2027", title: "Akad", body: "Kami menutup satu bab dan membuka bab baru, bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Sunda Kelapa", address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat" },
    { name: "Resepsi", date: "2027-09-11T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "The Dharmawangsa Jakarta", address: "Jl. Brawijaya Raya No. 26, Pulo, Kebayoran Baru, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a85.webp", "/themes/img/a110.webp", "/themes/img/r57.webp", "/themes/img/a84.webp", "/themes/img/a118.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0613 7788 42", account_name: "Nadia Khairunnisa Harahap" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7209 4411 06", account_name: "Hamzah Al-Fatih Wibisono" },
  ],
  guestName: "Bapak H. Ridwan Syamsudin & Keluarga",
  guestTable: "Meja Onyx 7",
  extras: {
    quote: { text: "Mereka adalah pakaian bagimu, dan kamu adalah pakaian bagi mereka.", source: "QS. Al-Baqarah: 187" },
    rundown: { items: [
      { time: "19.00", title: "Penyambutan tamu", note: "Iringan gambus akustik" },
      { time: "19.30", title: "Kedatangan kedua mempelai" },
      { time: "20.00", title: "Jamuan malam" },
      { time: "21.00", title: "Doa & foto bersama" },
    ] },
    dressCode: { note: "Formal malam: hitam, emas, atau abu arang.", colors: ["#111113", "#c7a256", "#4a4844", "#ece6da"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-11T09:00:00+07:00" },
    guestPass: {},
    family: { names: ["Kel. Besar Ir. H. Taufik Harahap", "Kel. Besar H. Bambang Wibisono"] },
  },
});
