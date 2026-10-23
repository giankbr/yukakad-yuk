import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Azizah", groom: "Fadli",
    brideFull: "Dayang Nur Azizah, S.Pd.", groomFull: "Uray Muhammad Fadli, S.H.",
    brideParents: "Putri bungsu dari\nBapak H. Abang Ismail & Ibu Hj. Siti Rahmah", groomParents: "Putra pertama dari\nBapak Uray Hamdan & Ibu Dayang Fatimah",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Seperti benang emas yang ditenun sehelai demi sehelai pada kain lunggi, semoga ikatan ini kian indah dari hari ke hari.",
  },
  eventLabel: "Walimatul 'Urs",
  date: "2027-08-14T09:00:00+07:00",
  place: "Balai Pertemuan Umum Sambas",
  address: "Jl. Pembangunan, Pasar Melayu, Kec. Sambas, Kab. Sambas, Kalimantan Barat",
  stories: [
    { date: "2018", title: "Satu Sekolah di Tepi Sungai", body: "Kami bersekolah di SMA yang sama di Sambas, setiap pagi menyeberang dengan sampan yang sama." },
    { date: "2024", title: "Bertemu Kembali", body: "Selepas merantau ke Pontianak, kami dipertemukan lagi di acara makan saprahan keluarga besar." },
    { date: "2027", title: "Menyatukan Dua Keluarga", body: "Dengan restu orang tua, lamaran diterima dan kami bersiap menuju hari akad di kampung halaman." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Jami' Sultan Muhammad Syafiuddin II", address: "Jl. Keraton, Desa Dalam Kaum, Kec. Sambas, Kab. Sambas" },
    { name: "Walimah & Makan Saprahan", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Pertemuan Umum Sambas", address: "Jl. Pembangunan, Pasar Melayu, Kec. Sambas, Kab. Sambas" },
  ],
  gallery: ["/themes/img/a61.webp", "/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2208 15", account_name: "Dayang Nur Azizah" },
    { id: "demo-kado", type: "address", address: "Jl. Gusti Hamzah No. 21, Desa Lorong, Kec. Sambas, Kab. Sambas 79462" },
  ],
  guestName: "Bapak H. Abdul Rahman & Keluarga",
  guestTable: "Saprah 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "09.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Tepung tawar", note: "Doa restu para tetua" },
      { time: "11.00", title: "Bersanding di pelaminan" },
      { time: "12.00", title: "Makan saprahan", note: "Duduk bersila, satu saprah untuk enam tamu" },
    ] },
    dressCode: { note: "Baju kurung, teluk belanga, atau kain lunggi. Ungu, merah tua, dan emas dipersilakan.", colors: ["#3d1533", "#8e1b3f", "#d2a64a", "#e8c24a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abang Ismail", "Kel. Besar Uray Hamdan", "Keluarga besar Dalam Kaum, Sambas"] },
  },
});
