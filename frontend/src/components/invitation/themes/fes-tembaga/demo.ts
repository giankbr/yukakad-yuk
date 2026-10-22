import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Fikri",
    brideFull: "Zahra Kamila Basyaiban, S.Ars.", groomFull: "Muhammad Fikri Alhabsyi, S.T.",
    brideParents: "Putri pertama dari\nBapak H. Anwar Basyaiban & Ibu Hj. Rugayah", groomParents: "Putra ketiga dari\nBapak H. Salim Alhabsyi & Ibu Hj. Nur Aini",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti lentera tembaga yang menebar cahaya lewat ribuan lubang kecil, semoga rumah kami kelak menerangi siapa saja yang singgah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-25T08:00:00+07:00",
  place: "Pendopo Rumah Atsiri",
  address: "Jl. Watu Gede, Plumbon, Tawangmangu, Kabupaten Karanganyar, Jawa Tengah",
  stories: [
    { date: "2021", title: "Studio Arsitektur", body: "Kami bertemu saat merestorasi sebuah rumah tua di Laweyan; Zahra menggambar ulang kusennya, Fikri menghitung ulang balok kayunya." },
    { date: "2025", title: "Lentera dari Pasar", body: "Fikri membawa pulang sebuah lentera tembaga dari pasar loak, lalu menyerahkannya bersama keluarga saat khitbah." },
    { date: "2027", title: "Akad", body: "Bismillah, kami menyalakan lentera itu bersama di rumah yang baru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-25T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Karanganyar", address: "Jl. Lawu No. 1, Karanganyar, Kabupaten Karanganyar, Jawa Tengah" },
    { name: "Walimatul 'Ursy", date: "2027-09-25T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Rumah Atsiri", address: "Jl. Watu Gede, Plumbon, Tawangmangu, Kabupaten Karanganyar" },
  ],
  gallery: ["/themes/img/a140.webp", "/themes/img/r57.webp", "/themes/img/r2.webp", "/themes/img/r58.webp", "/themes/img/r0.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7203 4419 82", account_name: "Zahra Kamila Basyaiban" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0153 7720 41", account_name: "Muhammad Fikri Alhabsyi" },
    { id: "demo-kado", type: "address", address: "Jl. Dr. Rajiman No. 402, Laweyan, Kota Surakarta 57148" },
  ],
  guestName: "Bapak H. Umar Assegaf & Keluarga",
  guestTable: "Meja Tembaga 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Iringan gambus & marawis" },
      { time: "11.30", title: "Kedatangan kedua mempelai" },
      { time: "12.00", title: "Jamuan", note: "Nasi kebuli, kambing oven & teh mint" },
      { time: "13.30", title: "Doa & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim formal bernuansa saffron, tembaga, dan merah bata.", colors: ["#e3a25c", "#8a4421", "#cf8a7a", "#f6e9d9"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Anwar Basyaiban", "Kel. Besar H. Salim Alhabsyi"] },
  },
});
