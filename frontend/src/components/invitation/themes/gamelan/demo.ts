import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Damar",
    brideFull: "Sekar Ayu Pratiwi, S.Sn.", groomFull: "Damar Wicaksono, S.Sn.",
    brideParents: "Putri kedua dari\nBapak Suharyanto & Ibu Sri Rejeki", groomParents: "Putra sulung dari\nBapak H. Widodo Prasetyo & Ibu Hj. Tutik Handayani",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti gong yang menutup setiap gendhing, kami ingin menjadi tempat pulang satu sama lain.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T08:00:00+07:00",
  place: "Pendopo Ndalem Sasono Mulyo",
  address: "Jl. Gondorasan, Baluwarti, Pasar Kliwon, Surakarta",
  stories: [
    { date: "2018", title: "Satu Rancakan", body: "Sekar menabuh saron, Damar di bangku kendang. Kami berkenalan di latihan karawitan ISI Surakarta, saling mencuri pandang di sela gendhing ladrang." },
    { date: "2022", title: "Pentas di Yogyakarta", body: "Selepas pentas di Pendopo Tamansiswa, Damar menunggu sampai semua gamelan dirapikan, lalu mengajak Sekar makan gudeg di Wijilan." },
    { date: "2026", title: "Lamaran", body: "Keluarga Damar datang ke Klaten membawa seserahan sederhana dan satu permintaan: izin menabuh gendhing yang sama seumur hidup." },
    { date: "2027", title: "Gong Ageng", body: "Dengan restu kedua keluarga, kami melangkah ke akad, diiringi gamelan dari sanggar tempat kami pertama bertemu." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Surakarta", address: "Jl. Masjid Agung, Kauman, Pasar Kliwon, Surakarta" },
    { name: "Panggih & Resepsi", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Ndalem Sasono Mulyo", address: "Jl. Gondorasan, Baluwarti, Pasar Kliwon, Surakarta" },
  ],
  gallery: ["/themes/img/a49.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a27.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0072 0110 4455 507", account_name: "Sekar Ayu Pratiwi" },
    { id: "demo-kado", type: "address", address: "Jl. Kenari No. 9, Kemlayan, Serengan, Surakarta 57151" },
  ],
  guestName: "Bapak Sunarto & Keluarga",
  guestTable: "Pendopo 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin", note: "Diiringi gendhing Kebo Giro" },
      { time: "11.30", title: "Upacara panggih & balangan gantal" },
      { time: "12.15", title: "Sungkeman" },
      { time: "12.45", title: "Klenengan & ramah tamah", note: "Gamelan Sanggar Ngesti Laras" },
    ] },
    dressCode: { note: "Batik atau kebaya. Nuansa merah bata, tembaga, dan cokelat tua dipersilakan.", colors: ["#8f2417", "#b98a3e", "#3b2414", "#efe2c8"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Suharyanto (Klaten)", "Kel. Besar Bpk. H. Widodo Prasetyo (Surakarta)", "Keluarga Sanggar Ngesti Laras"] },
  },
});
