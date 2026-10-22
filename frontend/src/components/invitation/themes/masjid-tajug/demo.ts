import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hanifah", groom: "Ghufron",
    brideFull: "Siti Hanifah Rahmawati, S.Pd.I.", groomFull: "Ahmad Ghufron Maulana, Lc.",
    brideParents: "Putri kedua dari\nBapak K.H. Abdul Mu'id & Ibu Hj. Nur Aini", groomParents: "Putra sulung dari\nBapak H. Masruri & Ibu Hj. Umi Kultsum",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Semoga rumah tangga kami seperti serambi masjid di pagi hari: teduh, terbuka bagi siapa saja, dan selalu dekat dengan panggilan-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-07-10T08:00:00+07:00",
  place: "Pendopo Kabupaten Kudus",
  address: "Jl. Simpang Tujuh No. 1, Kauman, Kota Kudus, Jawa Tengah",
  stories: [
    { date: "2017", title: "Ngaji Pasaran", body: "Kami pertama bertemu saat ngaji pasaran Ramadan di Kudus. Hanifah mencatat paling rapi, Ghufron selalu duduk paling belakang." },
    { date: "2025", title: "Khitbah", body: "Sepulang Ghufron dari Kairo, keluarganya datang bersilaturahmi dan menyampaikan khitbah. Alhamdulillah diterima dengan doa." },
    { date: "2027", title: "Akad di Bulan Muharram", body: "Dengan izin Allah, kami menyempurnakan separuh agama di kota tempat kami pertama kali bertemu." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Kudus", address: "Jl. Simpang Tujuh, Kauman, Kota Kudus, Jawa Tengah" },
    { name: "Walimatul 'Ursy", date: "2027-07-10T10:30:00+07:00", time: "10.30 – 14.00 WIB", venue: "Pendopo Kabupaten Kudus", address: "Jl. Simpang Tujuh No. 1, Kauman, Kota Kudus, Jawa Tengah" },
  ],
  gallery: ["/themes/img/r62.webp", "/themes/img/a64.webp", "/themes/img/r76.webp", "/themes/img/r14.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7177 8899 00", account_name: "Siti Hanifah Rahmawati" },
    { id: "demo-bri", type: "bank", bank_name: "BRI Syariah", account_number: "1002 3344 5566", account_name: "Ahmad Ghufron Maulana" },
  ],
  guestName: "Bapak K.H. Ma'ruf Hasyim & Keluarga",
  guestTable: "Serambi 2",
  extras: {
    quote: { text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu. Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya.", source: "QS. An-Nur: 32" },
    rundown: { items: [
      { time: "10.30", title: "Kirab manten", note: "Diiringi hadrah" },
      { time: "11.00", title: "Mauidhoh hasanah", note: "Oleh K.H. Ma'ruf Hasyim" },
      { time: "12.00", title: "Ramah tamah", note: "Soto kerbau & jenang Kudus" },
    ] },
    dressCode: { note: "Busana muslim. Warna kayu jati, bata, hijau sawo, dan krem dipersilakan.", colors: ["#7a4a26", "#a5482e", "#4f6b3a", "#f5ead6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar K.H. Abdul Mu'id", "Kel. Besar H. Masruri"] },
  },
});
