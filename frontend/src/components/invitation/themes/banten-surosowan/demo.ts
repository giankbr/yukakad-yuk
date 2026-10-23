import { makeDemo } from "../demo-base";

// Adat Banten (Muslim), Kota Serang: akad nikah di Masjid Agung Banten → walimah/resepsi di Serang.
export const demo = makeDemo({
  couple: {
    bride: "Nabila", groom: "Ilham",
    brideFull: "Nabila Khairunnisa, S.Ked.", groomFull: "Ilham Fadhilah Rahman, S.H.",
    brideParents: "Putri kedua dari\nBapak H. Tb. Ahmad Syarifuddin & Ibu Hj. Siti Maemunah", groomParents: "Putra sulung dari\nBapak Drs. H. Mukhlis Hidayat & Ibu Hj. Yuyun Yuningsih",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti bata-bata Surosowan yang tetap berdiri melewati zaman, semoga ikatan kami kokoh, sederhana, dan diberkahi Allah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-12T08:00:00+07:00",
  place: "Masjid Agung Banten",
  address: "Kawasan Banten Lama, Kel. Banten, Kec. Kasemen, Kota Serang, Banten",
  stories: [
    { date: "2020", title: "Kuliah Kerja di Kasemen", body: "Kami satu kelompok KKN di Banten Lama. Ilham bertugas mendata situs, Nabila membuka posko kesehatan di dekat menara." },
    { date: "2023", title: "Rabeg di Alun-alun Serang", body: "Selepas wisuda Nabila, kami makan rabeg di dekat alun-alun. Obrolan ringan malam itu berubah menjadi niat yang sungguh-sungguh." },
    { date: "Maret 2027", title: "Khitbah", body: "Keluarga Ilham datang melamar ke rumah keluarga Tb. Ahmad Syarifuddin, disambut doa para sesepuh dan sepiring jojorong." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Banten", address: "Kawasan Banten Lama, Kel. Banten, Kec. Kasemen, Kota Serang, Banten" },
    { name: "Walimatul 'Ursy", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Graha Pancaniti", address: "Jl. Brigjen K.H. Syam'un No. 5, Kel. Kotabaru, Kec. Serang, Kota Serang, Banten" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a26.webp", "/themes/img/r98.webp", "/themes/img/r42.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7188 2290 41", account_name: "Nabila Khairunnisa" },
    { id: "demo-bjb", type: "bank", bank_name: "Bank BJB Syariah", account_number: "5150 1022 3378 0", account_name: "Ilham Fadhilah Rahman" },
    { id: "demo-kado", type: "address", address: "Jl. Raya Banten Lama No. 17, Kel. Kasunyatan, Kec. Kasemen, Kota Serang, Banten 42191", account_name: "Keluarga H. Tb. Ahmad Syarifuddin" },
  ],
  guestName: "Bapak K.H. Abdul Hamid & Keluarga",
  guestTable: "Meja Surosowan 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Diiringi rampak bedug khas Banten" },
      { time: "11.30", title: "Pembacaan doa & sambutan keluarga" },
      { time: "12.00", title: "Jamuan makan", note: "Rabeg, sate bandeng, dan jojorong" },
      { time: "14.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim rapi. Nuansa ungu lembut, abu kebiruan, atau merah bata dipersilakan.", colors: ["#b9a9c4", "#7fa3a2", "#a5533c", "#f4efe6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Tb. Ahmad Syarifuddin", "Kel. Besar Drs. H. Mukhlis Hidayat"] },
  },
});
