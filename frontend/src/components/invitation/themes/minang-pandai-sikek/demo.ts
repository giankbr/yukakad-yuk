import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahmi", groom: "Fadhlan",
    brideFull: "Rahmi Yuliani Putri, S.Ds.", groomFull: "Fadhlan Hakim Sutan Mangkuto, S.T.",
    brideParents: "Putri sulung dari\nBapak H. Zulkifli Datuak Rajo Mangkuto & Ibu Hj. Yusnimar", groomParents: "Putra kedua dari\nBapak Drs. Afrizal & Ibu Elfi Rosneli",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Alam takambang jadi guru. Seperti benang emas yang ditenun helai demi helai, kami ingin merajut rumah tangga dengan sabar dan teliti.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T09:00:00+07:00",
  place: "Masjid Jamik Pandai Sikek",
  address: "Jorong Pagu-Pagu, Nagari Pandai Sikek, Kec. X Koto, Kabupaten Tanah Datar, Sumatera Barat",
  stories: [
    { date: "2019", title: "Di Rumah Tenun", body: "Fadhlan datang memotret penenun songket untuk tugas kuliah. Rahmi yang menjelaskan motif demi motif, dari pucuak rabuang sampai itiak pulang patang." },
    { date: "2025", title: "Maminang", body: "Keluarga Rahmi datang maminang ke rumah keluarga Fadhlan, membawa sirih di carano dan niat baik." },
    { date: "2027", title: "Baralek", body: "Dengan memohon rida Allah dan restu ninik mamak, kami menyatukan dua keluarga di kampung halaman." },
  ],
  events: [
    { name: "Malam Bainai", date: "2027-06-18T20:00:00+07:00", time: "20.00 – 22.00 WIB", venue: "Rumah Keluarga Mempelai Wanita", address: "Jorong Koto Tinggi, Nagari Pandai Sikek, Kabupaten Tanah Datar" },
    { name: "Akad Nikah", date: "2027-06-19T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Jamik Pandai Sikek", address: "Jorong Pagu-Pagu, Nagari Pandai Sikek, Kec. X Koto, Kabupaten Tanah Datar" },
    { name: "Baralek Gadang", date: "2027-06-20T11:00:00+07:00", time: "11.00 – 16.00 WIB", venue: "Gedung Pertemuan Panorama", address: "Jl. Panorama No. 7, Kayu Kubu, Guguk Panjang, Kota Bukittinggi" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r108.webp", "/themes/img/r1.webp", "/themes/img/a30.webp", "/themes/img/r16.webp"],
  gifts: [
    { id: "demo-bnag", type: "bank", bank_name: "Bank Nagari", account_number: "1002 0210 4471 88", account_name: "Rahmi Yuliani Putri" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7190 4473 12", account_name: "Fadhlan Hakim" },
  ],
  guestName: "Bapak H. Asril Datuak Bandaro & Keluarga",
  guestTable: "Meja Songket 5",
  extras: {
    quote: { text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu. Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya.", source: "QS. An-Nur: 32" },
    rundown: { items: [
      { time: "11.00", title: "Manjapuik marapulai", note: "Arak-arakan diiringi talempong dan gandang tambua" },
      { time: "11.45", title: "Penyambutan & pasambahan" },
      { time: "12.30", title: "Makan bajamba" },
      { time: "14.00", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana Minang atau busana muslim resmi. Hitam, merah, dan emas (warna marawa) dipersilakan.", colors: ["#1c1412", "#9a1f1c", "#d6a83e", "#f6efe2"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-19T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkifli Datuak Rajo Mangkuto", "Kel. Besar Drs. Afrizal"] },
  },
});
