import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Humaira", groom: "Yusuf",
    brideFull: "Humaira Az-Zahra Basalamah", groomFull: "Yusuf Abdullah Alatas, Lc.",
    brideParents: "Putri bungsu dari\nBapak H. Salim Basalamah & Ibu Hj. Syarifah Nur", groomParents: "Putra kedua dari\nBapak H. Hasan Alatas & Ibu Hj. Aminah Assegaf",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti mawar Taif yang mekar di lembah berbatu, semoga cinta kami tumbuh harum di tengah segala ujian, dan wangi doanya sampai kepada orang-orang yang kami sayangi.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-17T09:00:00+07:00",
  place: "Hotel Majapahit Surabaya, Ballroom Raya",
  address: "Jl. Tunjungan No. 65, Genteng, Surabaya, Jawa Timur",
  stories: [
    { date: "2021", title: "Oleh-oleh dari Thaif", body: "Sepulang umrah, keluarga Yusuf membawa sebotol air mawar Thaif untuk keluarga Humaira. Begitulah dua keluarga mulai akrab." },
    { date: "2026", title: "Khitbah", body: "Yusuf pulang dari Madinah dan datang bersama keluarganya ke Ampel. Lamaran diterima dengan senyum dan doa." },
    { date: "2027", title: "Musim Mawar", body: "Insyaallah akad kami bertepatan dengan musim panen mawar di Thaif, bulan yang paling harum." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Sunan Ampel", address: "Jl. Petukangan I, Ampel, Semampir, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-04-17T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Hotel Majapahit Surabaya, Ballroom Raya", address: "Jl. Tunjungan No. 65, Genteng, Surabaya, Jawa Timur" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r16.webp", "/themes/img/a111.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7177 4020 96", account_name: "Humaira Az-Zahra Basalamah" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 115 643", account_name: "Yusuf Abdullah Alatas" },
  ],
  guestName: "Bapak H. Umar Bawazier & Keluarga",
  guestTable: "Meja Ward 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan", note: "Diiringi gambus & marawis" },
      { time: "19.15", title: "Doa & nasihat pernikahan", note: "Habib Abdullah Al-Habsyi" },
      { time: "19.45", title: "Jamuan", note: "Nasi kebuli & teh mawar" },
    ] },
    dressCode: { note: "Gamis dan jubah bernuansa merah muda, dusty rose, atau batu pasir.", colors: ["#e48aa0", "#f6cbd3", "#c9b8a3", "#fbf1ee"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Basalamah", "Kel. Besar Alatas"] },
  },
});
