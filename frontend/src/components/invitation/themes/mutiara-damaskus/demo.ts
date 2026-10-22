import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Rayyan",
    brideFull: "Salma Putri Assegaf, S.Ds.", groomFull: "Rayyan Ahmad Baraqbah, S.E.",
    brideParents: "Putri kedua dari\nBapak H. Hasan Assegaf & Ibu Hj. Fatimah Alatas", groomParents: "Putra pertama dari\nBapak H. Umar Baraqbah & Ibu Hj. Khadijah",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a113.webp",
    note: "Seperti kerang mutiara yang ditatah satu per satu, kami ingin merangkai hari dengan sabar dan indah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-11-06T09:00:00+07:00",
  place: "Hotel Majapahit Surabaya",
  address: "Jl. Tunjungan No. 65, Genteng, Kota Surabaya",
  stories: [
    { date: "2022", title: "Kotak Bertatah", body: "Kami bertemu di sebuah pameran kriya di Ampel, sama-sama jatuh hati pada sebuah kotak kayu bertatah mutiara." },
    { date: "2026", title: "Khitbah", body: "Rayyan datang bersama keluarga, membawa kotak itu sebagai tanda kesungguhan." },
    { date: "2027", title: "Akad", body: "Bismillah, kami memulai perjalanan sebagai satu keluarga." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-11-06T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Nasional Al-Akbar", address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Kota Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-11-06T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "Hotel Majapahit Surabaya", address: "Jl. Tunjungan No. 65, Genteng, Kota Surabaya" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a99.webp", "/themes/img/a113.webp", "/themes/img/a26.webp", "/themes/img/a116.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 6619 30", account_name: "Salma Putri Assegaf" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7177 3305 18", account_name: "Rayyan Ahmad Baraqbah" },
    { id: "demo-kado", type: "address", address: "Jl. Nyamplungan Gg. 3 No. 12, Ampel, Semampir, Kota Surabaya 60151" },
  ],
  guestName: "Bapak H. Mahdi Alaydrus & Keluarga",
  guestTable: "Meja Mawar 5",
  extras: {
    quote: { text: "Dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.30", title: "Penyambutan tamu", note: "Iringan gambus & hadrah" },
      { time: "12.00", title: "Kedatangan kedua mempelai" },
      { time: "12.30", title: "Jamuan", note: "Nasi kebuli & kopi Arab" },
      { time: "13.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim formal dalam blush, krem, atau cokelat kayu.", colors: ["#e9b7ab", "#f5efe7", "#5e3a24", "#b98458"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Hasan Assegaf", "Kel. Besar H. Umar Baraqbah"] },
  },
});
