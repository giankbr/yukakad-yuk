import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gusti Ayu", groom: "Wisnu",
    brideFull: "Gusti Ayu Sekar Kedhaton, S.H.", groomFull: "Raden Mas Wisnu Hadikusumo, M.M.",
    brideParents: "Putri sulung dari\nBapak KPH. Suryo Hadiningrat & Ibu Raden Ayu Kusumawati", groomParents: "Putra kedua dari\nBapak Ir. RM. Bagus Hadikusumo & Ibu Endah Prihatini",
    bridePhoto: "/themes/img/a47.webp", groomPhoto: "/themes/img/a48.webp",
    note: "Hamemayu hayuning bawana — semoga rumah tangga kami turut memperindah dunia.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-20T09:00:00+07:00",
  place: "Bangsal Kepatihan",
  address: "Jl. Malioboro No. 16, Suryatmajan, Danurejan, Yogyakarta",
  stories: [
    { date: "2019", title: "Abdi Budaya", body: "Bertemu saat sama-sama menjadi relawan pagelaran budaya di Yogyakarta." },
    { date: "2023", title: "Menjaga Tradisi", body: "Kami belajar tata cara adat dari para sesepuh, sambil merencanakan masa depan." },
    { date: "2027", title: "Pahargyan Dalem", body: "Dengan restu keluarga besar, kami melangkah dalam upacara adat Yogyakarta." },
  ],
  events: [
    { name: "Ijab Kabul", date: "2027-11-20T08:00:00+07:00", time: "08.00 – 09.00 WIB", venue: "Masjid Gedhe Kauman", address: "Jl. Kauman, Ngupasan, Gondomanan, Yogyakarta" },
    { name: "Panggih & Kirab", date: "2027-11-20T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Bangsal Kepatihan", address: "Jl. Malioboro No. 16, Suryatmajan, Danurejan, Yogyakarta" },
    { name: "Resepsi", date: "2027-11-20T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Bangsal Kepatihan", address: "Jl. Malioboro No. 16, Suryatmajan, Danurejan, Yogyakarta" },
  ],
  gallery: ["/themes/img/a46.webp", "/themes/img/a47.webp", "/themes/img/a48.webp", "/themes/img/a34.webp", "/themes/img/a24.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4450 1234 56", account_name: "Gusti Ayu Sekar Kedhaton" },
    { id: "demo-kado", type: "address", address: "Jl. Rotowijayan No. 3, Kadipaten, Kraton, Yogyakarta 55132" },
  ],
  guestName: "Bapak KRT. Purbo Wijoyo & Keluarga",
  guestTable: "Bangsal 1",
  extras: {
    rundown: { items: [
      { time: "10.00", title: "Kirab kereta kencana", note: "Diiringi prajurit & gendhing Kebo Giro" },
      { time: "10.30", title: "Upacara panggih" },
      { time: "11.00", title: "Pangabekten (sungkeman)" },
    ] },
    dressCode: { note: "Busana Jawa resmi. Hijau tua, emas, dan hitam dipersilakan.", colors: ["#0f2a22", "#cfa652", "#1d4a3a", "#6e1a22"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-11-20T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar KPH. Suryo Hadiningrat", "Kel. Besar Ir. RM. Bagus Hadikusumo"] },
  },
});
