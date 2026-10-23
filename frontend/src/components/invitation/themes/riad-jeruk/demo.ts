import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Syifa", groom: "Rayhan",
    brideFull: "Syifa Az-Zahra Maulani, S.Ars.", groomFull: "Rayhan Akbar Firdaus, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Dedi Maulana & Ibu Hj. Rina Kartika", groomParents: "Putra pertama dari\nBapak Ir. Firdaus Hamzah & Ibu Nurul Aini",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti pohon jeruk di tengah halaman: berakar tenang, berbuah manis, dan meneduhkan siapa pun yang singgah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-17T08:00:00+07:00",
  place: "Graha Andalusia",
  address: "Jl. Pajajaran No. 88, Baranangsiang, Bogor Timur, Kota Bogor",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2020", title: "Satu Studio", body: "Kami bertemu di studio arsitektur yang sama, mengerjakan sketsa sebuah rumah berhalaman tengah di Bogor." },
    { date: "2024", title: "Ta'aruf", body: "Lewat perantara guru mengaji Syifa, kami berta'aruf dengan tenang dan saling mengenal keluarga." },
    { date: "2026", title: "Khitbah", body: "Rayhan datang bersama keluarga di bawah pohon jeruk di halaman rumah Syifa. Jawabannya: bismillah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Bantarjati, Bogor Utara, Kota Bogor" },
    { name: "Walimatul 'Ursy", date: "2027-04-17T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Andalusia", address: "Jl. Pajajaran No. 88, Baranangsiang, Bogor Timur, Kota Bogor" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/r57.webp", "/themes/img/a22.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 2041 63", account_name: "Syifa Az-Zahra Maulani" },
    { id: "demo-bca", type: "bank", bank_name: "BCA Syariah", account_number: "0451 2290 77", account_name: "Rayhan Akbar Firdaus" },
    { id: "demo-kado", type: "address", address: "Jl. Kenanga Raya No. 14, Tegallega, Bogor Tengah, Kota Bogor 16129" },
  ],
  guestName: "Bapak H. Zainal Arifin & Keluarga",
  guestTable: "Meja Jeruk 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "08.20", title: "Ijab kabul", note: "Keluarga inti & saksi" },
      { time: "08.50", title: "Nasihat pernikahan & doa" },
      { time: "11.00", title: "Walimah dibuka", note: "Hidangan teh mint & kue kering" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa pastel: merah jambu pudar, hijau mint, biru langit, atau krem.", colors: ["#e6b3a2", "#a3cfbd", "#93bcd2", "#f3ebdd"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dedi Maulana", "Kel. Besar Ir. Firdaus Hamzah"] },
  },
});
