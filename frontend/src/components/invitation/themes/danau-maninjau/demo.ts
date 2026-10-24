import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsa", groom: "Reza",
    brideFull: "Salsabila Annisa Putri, S.Pd.", groomFull: "Muhammad Reza Pratama, S.T.",
    brideParents: "Putri sulung dari\nBapak H. Syahrial Datuak Rajo Bujang & Ibu Hj. Nurhayati", groomParents: "Putra kedua dari\nBapak Zulfikri & Ibu Yusmaniar",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Empat puluh empat kelok kami turuni untuk sampai ke tepi danau ini. Kini kami ingin melangkah bersama, satu kelok demi satu kelok.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-07-10T08:30:00+07:00",
  place: "Masjid Raya Bayur",
  address: "Jorong Bayur, Nagari Bayur, Kec. Tanjung Raya, Kab. Agam, Sumatera Barat",
  stories: [
    { date: "Agustus 2021", title: "Tanjakan Kelok 44", body: "Reza ikut gowes bersama komunitas sepeda Bukittinggi. Di kelok ke-27 rantainya putus, dan Salsa yang sedang menjaga pos minum membantu mencarikan bengkel." },
    { date: "2023", title: "Sore di Tepi Danau", body: "Kami sering bertemu di lapau kopi dekat dermaga Bayur, membicarakan murid-murid Salsa dan proyek jalan Reza sambil menunggu matahari turun di balik dinding kawah." },
    { date: "Maret 2027", title: "Batimbang Tando", body: "Keluarga Reza datang ke rumah gadang kaum. Ninik mamak bermufakat, tanda dipertukarkan, dan hari baik pun ditetapkan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Raya Bayur", address: "Jorong Bayur, Nagari Bayur, Kec. Tanjung Raya, Kab. Agam, Sumatera Barat" },
    { name: "Baralek di Rumah Gadang", date: "2027-07-10T11:00:00+07:00", time: "11.00 – 16.00 WIB", venue: "Rumah Gadang Kaum Datuak Rajo Bujang", address: "Jorong Bayur, Nagari Bayur, Kec. Tanjung Raya, Kab. Agam (tepi Danau Maninjau)" },
    { name: "Resepsi Bukittinggi", date: "2027-07-17T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Balai Sidang Bung Hatta", address: "Jl. Jenderal Sudirman, Belakang Balok, Kec. Aur Birugo Tigo Baleh, Kota Bukittinggi" },
  ],
  gallery: ["/themes/img/a66.webp", "/themes/img/a64.webp", "/themes/img/a72.webp", "/themes/img/r104.webp", "/themes/img/a63.webp"],
  gifts: [
    { id: "demo-nagari", type: "bank", bank_name: "Bank Nagari", account_number: "1001 0210 3845 77", account_name: "Salsabila Annisa Putri" },
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7190 4432 18", account_name: "Muhammad Reza Pratama" },
    { id: "demo-kado", type: "address", address: "Rumah Gadang Kaum Datuak Rajo Bujang, Jorong Bayur, Nagari Bayur, Kec. Tanjung Raya, Kab. Agam 26471", account_name: "Keluarga H. Syahrial" },
  ],
  guestName: "Bapak H. Asrul Datuak Sinaro & Keluarga",
  guestTable: "Meja Kelok 12",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Manjapuik marapulai", note: "Rombongan anak daro menjemput dengan carano dan sirih" },
      { time: "11.45", title: "Pasambahan adat", note: "Petatah-petitih ninik mamak kedua kaum" },
      { time: "12.30", title: "Makan bajamba", note: "Rendang, gulai ikan rinuak, dan pangek sasau khas Maninjau" },
      { time: "15.30", title: "Doa penutup & foto keluarga" },
    ] },
    dressCode: { note: "Busana muslim rapi bernuansa Maninjau: biru danau, hijau bukit, dan kuning padi.", colors: ["#2a5f8f", "#4f8a4a", "#d9b552", "#a85e38"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syahrial Datuak Rajo Bujang", "Kel. Besar Zulfikri", "Ninik Mamak Kaum Bayur"] },
  },
});
