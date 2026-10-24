import { makeDemo } from "../demo-base";

// Pernikahan adat Jawa di desa penenun lurik Pedan–Cawas, Klaten: kain lurik ATBM, sawah, dan Merapi di kejauhan.
export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Bayu",
    brideFull: "Larasati Wulandari, S.Ds.", groomFull: "Bayu Aji Prasetyo, S.P.",
    brideParents: "Putri pertama dari\nBapak Suparno & Ibu Sri Lestari", groomParents: "Putra kedua dari\nBapak H. Mulyono & Ibu Hj. Tri Handayani",
    bridePhoto: "/themes/img/a47.webp", groomPhoto: "/themes/img/a48.webp",
    note: "Lungsin dan pakan tidak pernah searah, tapi justru karena saling menyilang, kainnya jadi kuat.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T08:00:00+07:00",
  place: "Pendapa Keluarga Bapak Suparno",
  address: "Dukuh Mlese RT 02/RW 04, Desa Tlingsing, Kec. Cawas, Kabupaten Klaten, Jawa Tengah",
  stories: [
    { date: "2020", title: "Benang yang Kusut", body: "Bayu datang ke bengkel tenun bapaknya Laras untuk survei tugas akhir pertanian. Pulangnya justru belajar menggulung benang, tangannya penuh kusut." },
    { date: "2023", title: "Panen dan Pameran", body: "Laras memamerkan lurik desa di Jogja, Bayu membantu mengangkut kain sepulang panen. Sejak itu jadwal panen dan pameran selalu kami sesuaikan." },
    { date: "2027", title: "Satu Lembar Lurik", body: "Dengan restu kedua keluarga, kami memasang lungsin baru di alat tenun yang sama, untuk ditenun bersama seumur hidup." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jami' Al-Huda Tlingsing", address: "Jl. Pedan–Cawas, Desa Tlingsing, Kec. Cawas, Kabupaten Klaten" },
    { name: "Panggih & Resepsi", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendapa Keluarga Bapak Suparno", address: "Dukuh Mlese RT 02/RW 04, Desa Tlingsing, Kec. Cawas, Kabupaten Klaten" },
    { name: "Ngunduh Mantu", date: "2027-06-26T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Gedung Serbaguna Delanggu", address: "Jl. Raya Solo–Yogyakarta, Kec. Delanggu, Kabupaten Klaten" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/a50.webp", "/themes/img/a49.webp", "/themes/img/r61.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0217 0100 4321 506", account_name: "Larasati Wulandari" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 0412 63", account_name: "Bayu Aji Prasetyo" },
    { id: "demo-kado", type: "address", address: "Dukuh Mlese RT 02/RW 04, Desa Tlingsing, Kec. Cawas, Klaten 57463" },
  ],
  guestName: "Bapak Wiryo Sudarmo & Keluarga",
  guestTable: "Meja Lungsin 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Upacara panggih", note: "Balangan gantal, wiji dadi, dan sindur" },
      { time: "12.00", title: "Sungkeman & doa" },
      { time: "12.30", title: "Kembul bujana", note: "Nasi liwet, garang asem, dan wedang secang" },
    ] },
    dressCode: { note: "Berbusana lurik atau batik. Nila, cokelat soga, dan krem dipersilakan.", colors: ["#2d3b5e", "#7a4e2c", "#ece0c4", "#211c19"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak Suparno", "Kel. Besar Bapak H. Mulyono", "Paguyuban Penenun Lurik Tlingsing"] },
  },
});
