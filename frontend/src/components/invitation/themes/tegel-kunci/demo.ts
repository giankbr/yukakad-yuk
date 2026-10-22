import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Ihsan",
    brideFull: "Larasati Kusuma Wardhani, S.Ars.", groomFull: "Muhammad Ihsan Prasetyo, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Bambang Hadiwiryo & Ibu Hj. Sri Rejeki", groomParents: "Putra kedua dari\nBapak Drs. H. Slamet Riyadi & Ibu Hj. Umi Kalsum",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Di teras rumah Eyang, di atas tegel kunci yang sama tempat kami dulu bermain gundu, kami ingin memulai babak baru. Mampirlah, kursi rotannya sudah disiapkan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-19T08:00:00+07:00",
  place: "Rumah Lawas Keluarga Hadiwiryo",
  address: "Jl. Mondorakan No. 41, Prenggan, Kotagede, Kota Yogyakarta",
  stories: [
    { date: "1999", title: "Tetangga Satu Gang", body: "Rumah kami hanya dipisah tiga pintu di gang Kotagede. Teras berubin tegel milik Eyang jadi tempat main kami setiap sore." },
    { date: "2024", title: "Bertemu Lagi", body: "Setelah lama merantau, kami bertemu lagi saat sama-sama ikut merestorasi rumah-rumah tua di kampung halaman." },
    { date: "Desember 2026", title: "Lamaran di Teras", body: "Keluarga Ihsan datang membawa seserahan dan duduk di kursi rotan yang sama. Lamaran diterima dengan teh poci dan haru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Gedhe Mataram Kotagede", address: "Jl. Watu Gilang, Jagalan, Banguntapan, Bantul, DI Yogyakarta" },
    { name: "Walimatul 'Ursy", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Lawas Keluarga Hadiwiryo", address: "Jl. Mondorakan No. 41, Prenggan, Kotagede, Kota Yogyakarta" },
  ],
  gallery: ["/themes/img/r70.webp", "/themes/img/r74.webp", "/themes/img/r62.webp", "/themes/img/r86.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7166 2045 1187", account_name: "Larasati Kusuma Wardhani" },
    { id: "demo-bpd", type: "bank", bank_name: "BPD DIY Syariah", account_number: "802 211 004 563", account_name: "Muhammad Ihsan Prasetyo" },
    { id: "demo-kado", type: "address", address: "Jl. Mondorakan No. 41, Prenggan, Kotagede, Kota Yogyakarta 55172", account_name: "Keluarga H. Bambang Hadiwiryo" },
  ],
  guestName: "Bapak H. Joko Santoso & Keluarga",
  guestTable: "Teras Depan",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, agar kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab manten ke teras", note: "Iringan shalawat" },
      { time: "11.30", title: "Sambutan keluarga" },
      { time: "12.00", title: "Ramah tamah", note: "Gudeg, wedang secang, jajan pasar" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Batik atau kebaya sederhana bernuansa tegel: hijau toska, bata, kunyit, dan krem.", colors: ["#2f6664", "#b65a3c", "#cf9d3a", "#ece2cc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Bambang Hadiwiryo", "Kel. Besar Drs. H. Slamet Riyadi"] },
  },
});
