import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Bayu",
    brideFull: "Sekar Ayu Larasati, S.Pd.", groomFull: "Muhammad Bayu Prasetyo, S.P.",
    brideParents: "Putri bungsu dari\nBapak H. Slamet Riyadi & Ibu Hj. Sumiati", groomParents: "Putra kedua dari\nBapak Sugeng Wahyudi & Ibu Endang Lestari",
    bridePhoto: "/themes/img/a36.webp", groomPhoto: "/themes/img/a35.webp",
    note: "Seperti kopi yang tumbuh perlahan di kaki Ijen, semoga cinta kami matang dalam sabar dan syukur.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-14T08:00:00+07:00",
  place: "Balai Adat Desa Kemiren",
  address: "Jl. Raya Kemiren, Kemiren, Kec. Glagah, Kabupaten Banyuwangi",
  stories: [
    { date: "2019", title: "Panen Kopi", body: "Bayu sedang meneliti kebun kopi rakyat di lereng Ijen ketika Sekar memandu rombongan mahasiswa ke desanya." },
    { date: "2023", title: "Sepuluh Ewu Cangkir", body: "Di malam festival ngopi di Kemiren, kami duduk di serambi rumah Osing dan berbagi cerita sampai larut." },
    { date: "2027", title: "Menuju Akad", body: "Dengan ridha Allah dan restu kedua keluarga, kami memantapkan langkah menuju pernikahan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Baiturrahman", address: "Jl. Jenderal Sudirman, Kepatihan, Kec. Banyuwangi, Kabupaten Banyuwangi" },
    { name: "Walimatul 'Ursy", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Adat Desa Kemiren", address: "Jl. Raya Kemiren, Kemiren, Kec. Glagah, Kabupaten Banyuwangi" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a22.webp", "/themes/img/a64.webp", "/themes/img/a36.webp", "/themes/img/a35.webp", "/themes/img/a33.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0123 01 004567 50 8", account_name: "Sekar Ayu Larasati" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 3344 55", account_name: "Muhammad Bayu Prasetyo" },
  ],
  guestName: "Bapak H. Abdul Rohim & Keluarga",
  guestTable: "Meja Kopi 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Diiringi gamelan angklung paglak" },
      { time: "11.30", title: "Kirab kedua mempelai" },
      { time: "12.00", title: "Ramah tamah", note: "Pecel pitik & kopi Osing" },
      { time: "13.30", title: "Doa bersama & foto keluarga" },
    ] },
    dressCode: { note: "Busana muslim atau batik Banyuwangi. Hitam, krem, dan merah bata dipersilakan.", colors: ["#1d1712", "#efe2c6", "#a5322a", "#5f7a3c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Slamet Riyadi", "Kel. Besar Sugeng Wahyudi"] },
  },
});
