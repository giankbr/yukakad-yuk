import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinasih", groom: "Bagas",
    brideFull: "Sekar Ayu Kinasih, S.Sn.", groomFull: "Bagas Prasetyo Wicaksono, S.H.",
    brideParents: "Putri kedua dari\nBapak Drs. Hadi Sumarno & Ibu Sri Rahayu Ningsih", groomParents: "Putra pertama dari\nBapak Ir. Wahyu Wicaksono & Ibu Endang Retno Palupi",
    bridePhoto: "/themes/img/a36.webp", groomPhoto: "/themes/img/a35.webp",
    note: "Kados batik Sidomukti ingkang dipun agem ing dinten punika, mugi gesang kita dados mukti: mulya, tentrem, lan migunani tumrap sesami.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T08:00:00+07:00",
  place: "Pendhapi Gedhe Balaikota Surakarta",
  address: "Jl. Jenderal Sudirman No. 2, Kampung Baru, Pasar Kliwon, Kota Surakarta",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2019", title: "Sanggar Batik Laweyan", body: "Kami pertama bertemu di kelas membatik tulis di Laweyan. Kinasih mengajar canting, Bagas murid yang paling sering menumpahkan malam." },
    { date: "2024", title: "Nontoni", body: "Keluarga Bagas sowan ke Kauman untuk berkenalan, disambut wedang uwuh dan serabi Notosuman." },
    { date: "2027", title: "Paningsetan", body: "Kain Sidomukti ini menjadi paningset, tanda ikatan dua keluarga menuju akad dan panggih." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-25T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Surakarta", address: "Jl. Masjid Agung, Kauman, Pasar Kliwon, Kota Surakarta" },
    { name: "Panggih & Resepsi", date: "2027-09-25T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendhapi Gedhe Balaikota Surakarta", address: "Jl. Jenderal Sudirman No. 2, Kampung Baru, Pasar Kliwon, Kota Surakarta" },
  ],
  gallery: ["/themes/img/a49.webp", "/themes/img/a36.webp", "/themes/img/a35.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0587 0102 2027 503", account_name: "Sekar Ayu Kinasih" },
    { id: "demo-kado", type: "address", address: "Jl. Kauman Gg. Trayeman No. 12, Kauman, Pasar Kliwon, Kota Surakarta 57112" },
  ],
  guestName: "Bapak Dr. Suryo Hadinoto & Keluarga",
  guestTable: "Meja Sidomukti 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Upacara panggih", note: "Balangan gantal, wiji dadi, sindur binayang" },
      { time: "11.45", title: "Sungkeman kepada kedua orang tua" },
      { time: "12.15", title: "Kirab & resepsi", note: "Diiringi gendhing Kebo Giro" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana Jawa atau batik. Nuansa sogan, krem, dan cokelat tua dipersilakan.", colors: ["#6e4322", "#efdfbf", "#2b1d14", "#b07a3a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-25T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Drs. Hadi Sumarno", "Kel. Besar Ir. Wahyu Wicaksono", "Trah Mangunharjo, Laweyan"] },
  },
});
