import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Annisa", groom: "Fadhil",
    brideFull: "Annisa Rahmadani Putri, S.H.", groomFull: "Muhammad Fadhil Akbar, S.Kom.",
    brideParents: "Putri kedua dari\nBapak H. Andi Rahman & Ibu Hj. Nurlela",
    groomParents: "Putra sulung dari\nBapak H. Burhanuddin & Ibu Hj. Siti Aisyah",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Di antara langit senja dan laut yang tenang, kami berjanji menjadi bayangan yang saling memantulkan kebaikan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T16:00:00+08:00",
  place: "Anjungan Pantai Losari",
  address: "Jl. Penghibur, Losari, Ujung Pandang, Kota Makassar",
  stories: [
    { date: "2022", title: "Senja di Anjungan", body: "Kami sama-sama datang untuk salat Magrib di masjid tepi laut. Selepas salat, hujan turun dan kami berbagi satu payung sampai ke parkiran." },
    { date: "2025", title: "Ta'aruf", body: "Dengan perantaraan sahabat pengajian, kami saling mengenal dengan niat baik dan restu kedua orang tua." },
    { date: "Juli 2027", title: "Mappettuada", body: "Keluarga Fadhil datang melamar; tanggal baik ditetapkan dan doa dipanjatkan bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Terapung Amirul Mukminin", address: "Jl. Penghibur, Losari, Ujung Pandang, Kota Makassar" },
    { name: "Resepsi Senja", date: "2027-10-16T16:00:00+08:00", time: "16.00 – 19.00 WITA", venue: "Anjungan Pantai Losari", address: "Jl. Penghibur, Losari, Ujung Pandang, Kota Makassar" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r12.webp", "/themes/img/r109.webp", "/themes/img/a21.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 8836 42", account_name: "Annisa Rahmadani Putri" },
    { id: "demo-bca", type: "bank", bank_name: "BCA Syariah", account_number: "0581 3302 77", account_name: "Muhammad Fadhil Akbar" },
  ],
  guestName: "Bapak H. Abdul Gaffar & Keluarga",
  guestTable: "Meja Dermaga 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu", note: "Di tepi anjungan" },
      { time: "16.45", title: "Doa & sambutan keluarga" },
      { time: "17.30", title: "Jeda salat Magrib berjamaah" },
      { time: "18.15", title: "Santap malam", note: "Coto & pisang epe" },
    ] },
    dressCode: { note: "Busana muslim bernuansa senja: jingga lembut, mauve, dan biru malam.", colors: ["#f0a865", "#bf7280", "#5b4677", "#2b2a52"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Andi Rahman", "Kel. Besar H. Burhanuddin"] },
  },
});
