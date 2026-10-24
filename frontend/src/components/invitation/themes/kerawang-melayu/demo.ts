import { makeDemo } from "../demo-base";

// Walimatul 'urus Melayu Riau di Pekanbaru: akad di masjid, bersanding di balai adat berukir kerawang.
export const demo = makeDemo({
  couple: {
    bride: "Aina", groom: "Faris",
    brideFull: "Nurul Aina Syafitri, S.Ars.", groomFull: "Muhammad Faris Hakimi, S.T.",
    brideParents: "Puteri bongsu dari\nBapak H. Zulkarnain Effendi & Ibu Hj. Rosnah", groomParents: "Putera sulung dari\nBapak Tengku Azman & Ibu Syarifah Noraini",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Kami bertemu di bengkel ukir kayu cengal, sama-sama belajar bahwa ukiran yang indah justru lahir dari bagian yang dilubangi: tempat cahaya bisa masuk.",
  },
  eventLabel: "Walimatul 'Urus",
  date: "2027-08-14T08:00:00+07:00",
  place: "Masjid Raya An-Nur Pekanbaru",
  address: "Jl. Hang Tuah No. 1, Sumahilang, Kec. Pekanbaru Kota, Kota Pekanbaru, Riau",
  stories: [
    { date: "2022", title: "Bengkel Ukir di Siak", body: "Aina sedang meneliti ukiran tebuk tembus rumah-rumah lama di Siak untuk tugas akhirnya. Faris, relawan pemugaran, meminjamkan pahatnya yang paling kecil." },
    { date: "2024", title: "Sepanjang Sungai Siak", body: "Kami menyusuri rumah-rumah panggung tepian sungai, menggambar ulang panel kerawang yang hampir lapuk, dan mulai saling bercerita tentang rumah impian." },
    { date: "Maret 2027", title: "Merisik & Meminang", body: "Keluarga Faris datang merisik dengan tepak sirih. Pinangan diterima dengan pantun berbalas, dan tarikh bersanding pun disepakati." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya An-Nur Pekanbaru", address: "Jl. Hang Tuah No. 1, Sumahilang, Kec. Pekanbaru Kota, Kota Pekanbaru, Riau" },
    { name: "Majlis Bersanding", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Adat Melayu Riau", address: "Jl. Diponegoro, Suka Mulia, Kec. Sail, Kota Pekanbaru, Riau" },
  ],
  gallery: ["/themes/img/a61.webp", "/themes/img/a43.webp", "/themes/img/a72.webp", "/themes/img/a63.webp"],
  gifts: [
    { id: "demo-riaukepri", type: "bank", bank_name: "Bank Riau Kepri Syariah", account_number: "811 02 14526", account_name: "Nurul Aina Syafitri" },
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7208 1199 43", account_name: "Muhammad Faris Hakimi" },
    { id: "demo-kado", type: "address", address: "Jl. Durian Gg. Cengal No. 7, Labuh Baru Timur, Kec. Payung Sekaki, Kota Pekanbaru 28291", account_name: "Keluarga H. Zulkarnain" },
  ],
  guestName: "Bapak Datuk H. Ismail Saleh & Keluarga",
  guestTable: "Meja Cengal 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Berarak & silat pengantin", note: "Diiringi kompang dan bunga manggar" },
      { time: "11.30", title: "Bersanding & tepung tawar", note: "Oleh keluarga dan tetua adat" },
      { time: "12.15", title: "Jamuan makan beradat", note: "Gulai ikan patin, asam pedas, dan bolu kemojo" },
      { time: "14.30", title: "Doa selamat & berbalas pantun" },
    ] },
    dressCode: { note: "Baju kurung dan teluk belanga, warna kayu cengal, kuning diraja, krem, dan hijau daun.", colors: ["#7a3a18", "#d9a521", "#efe2c8", "#3f6b5e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkarnain Effendi", "Kel. Besar Tengku Azman", "Lembaga Adat Kampung Siak"] },
  },
});
