import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Ilham",
    brideFull: "Fatimah Az-Zahra Rahmadani, S.Ars.", groomFull: "Muhammad Ilham Hakim, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Rahmadi & Ibu Hj. Siti Nurjanah", groomParents: "Putra sulung dari\nBapak Drs. H. Abdul Hakim & Ibu Hj. Ratna Kusumawati",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti cahaya yang turun dari puncak kubah, semoga rahmat-Nya menaungi setiap sudut rumah yang akan kami bangun.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-14T08:00:00+07:00",
  place: "Aula Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung",
  stories: [
    { date: "2020", title: "Satu Studio", body: "Kami bertemu di studio arsitektur saat mengukur ulang ornamen sebuah masjid tua di Bandung. Zahra menggambar, Ilham menghitung." },
    { date: "2024", title: "Ta'aruf", body: "Setelah lama berteman, Ilham memberanikan diri bersilaturahmi ke rumah keluarga Zahra, didampingi kedua orang tuanya." },
    { date: "2027", title: "Menuju Akad", body: "Dengan restu kedua keluarga, kami menyempurnakan separuh agama di bulan yang teduh." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung" },
    { name: "Walimah", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a30.webp", "/themes/img/r82.webp", "/themes/img/a26.webp", "/themes/img/r56.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Fatimah Az-Zahra Rahmadani" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0987 6543", account_name: "Muhammad Ilham Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Barat No. 18, Cibeunying Kaler, Bandung 40191" },
  ],
  guestName: "Bapak H. Ridwan Kamaludin & Keluarga",
  guestTable: "Meja Kubah 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Jamuan & ramah tamah" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim yang santun. Nuansa putih gading, krem, dan emas pucat dipersilakan.", colors: ["#f7f3ea", "#e8dcc4", "#d9b871", "#8a6c3a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Rahmadi", "Kel. Besar Drs. H. Abdul Hakim"] },
  },
});
