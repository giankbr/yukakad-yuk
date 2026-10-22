import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Hanif",
    brideFull: "Zahra Nailul Muna, S.Pd.I.", groomFull: "Muhammad Hanif Al-Ghazali, Lc.",
    brideParents: "Putri pertama dari\nBapak KH. Ahmad Sya'roni & Ibu Hj. Siti Khotijah", groomParents: "Putra ketiga dari\nBapak H. Abdul Muhaimin & Ibu Hj. Nur Laili",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti bata merah yang disusun tanpa perekat namun berdiri berabad-abad, semoga ikatan kami kokoh karena saling menopang.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-09T08:00:00+07:00",
  place: "Masjid Al-Aqsa Menara Kudus",
  address: "Jl. Menara, Kauman, Kec. Kota Kudus, Kabupaten Kudus, Jawa Tengah",
  stories: [
    { date: "2018", title: "Satu Majelis", body: "Kami sama-sama mengikuti kajian kitab di serambi masjid tua Kudus, duduk di sisi yang berbeda dan hanya saling tahu nama." },
    { date: "2025", title: "Pulang dari Kairo", body: "Hanif kembali dari Al-Azhar dan mengajar di madrasah tempat Zahra bertugas. Para guru sepuh yang lebih dulu tersenyum." },
    { date: "Juli 2027", title: "Khitbah", body: "Keluarga Hanif datang mengkhitbah selepas Isya, membawa jenang Kudus dan niat baik." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Aqsa Menara Kudus", address: "Jl. Menara, Kauman, Kec. Kota Kudus, Kabupaten Kudus, Jawa Tengah" },
    { name: "Walimatul 'Ursy", date: "2027-10-09T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Kabupaten Kudus", address: "Jl. Simpang Tujuh No. 1, Kec. Kota Kudus, Kabupaten Kudus, Jawa Tengah" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/r57.webp", "/themes/img/r64.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7180 2291 46", account_name: "Zahra Nailul Muna" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0391 7765 20", account_name: "Muhammad Hanif" },
    { id: "demo-kado", type: "address", address: "Jl. Sunan Kudus Gg. 3 No. 12, Kauman, Kec. Kota Kudus, Kabupaten Kudus 59315", account_name: "Keluarga KH. Ahmad Sya'roni" },
  ],
  guestName: "Bapak KH. Ma'ruf Asnawi & Keluarga",
  guestTable: "Serambi Barat",
  extras: {
    quote: { text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu. Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya.", source: "QS. An-Nur: 32" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Iringan rebana dan shalawat" },
      { time: "11.30", title: "Mauidhoh hasanah", note: "KH. Ma'ruf Asnawi" },
      { time: "12.15", title: "Ramah tamah", note: "Soto Kudus dan jenang" },
      { time: "13.45", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim rapi. Merah bata, hijau tegel, krem, dan biru keramik dipersilakan.", colors: ["#b5502f", "#2f7a5c", "#f4ece0", "#2f4f8f"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar KH. Ahmad Sya'roni", "Kel. Besar H. Abdul Muhaimin"] },
  },
});
