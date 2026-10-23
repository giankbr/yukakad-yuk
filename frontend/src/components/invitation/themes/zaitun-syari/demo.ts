import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Irfan",
    brideFull: "Zahra Khairunnisa, S.Farm.", groomFull: "Irfan Maulana Hakim, S.Kom.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Syarifuddin & Ibu Hj. Rahmawati",
    groomParents: "Putra pertama dari\nBapak Dr. Ir. Hasan Basri & Ibu Nurul Fadhilah",
    note: "Seperti zaitun yang tumbuh perlahan dan berbuah setelah musim yang panjang, semoga rumah kami teduh, bercahaya, dan memberi manfaat.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-09T08:00:00+07:00",
  place: "Masjid Raya Bogor",
  address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Bogor Timur, Kota Bogor",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Satu Kajian", body: "Kami sama-sama menjadi relawan kajian pekanan di masjid kampus, dari sisi tirai yang berbeda." },
    { date: "2026", title: "Ta'aruf", body: "Melalui guru mengaji masing-masing, biodata kami dipertukarkan dan dua keluarga bersilaturahmi di Baranangsiang." },
    { date: "Juni 2027", title: "Khitbah", body: "Keluarga Irfan datang dengan niat baik dan sekeranjang buah. Dengan izin Allah, lamaran diterima." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Bogor Timur, Kota Bogor" },
    { name: "Walimatul 'Ursy", date: "2027-10-09T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Kemuning Gading", address: "Jl. Kemuning No. 3, Tegallega, Bogor Tengah, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7201 4438 9015", account_name: "Zahra Khairunnisa" },
    { id: "demo-muamalat", type: "bank", bank_name: "Bank Muamalat", account_number: "3420 0661 2790", account_name: "Irfan Maulana Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Bangbarung Raya No. 21, Bantarjati, Bogor Utara, Kota Bogor 16153", account_name: "Keluarga H. Ahmad Syarifuddin" },
  ],
  guestName: "Ibu Hj. Maryam Lubis & Keluarga",
  guestTable: "Meja Zaitun 3",
  extras: {
    quote: { text: "Allah adalah cahaya langit dan bumi... yang dinyalakan dengan minyak dari pohon yang diberkahi, yaitu pohon zaitun.", source: "QS. An-Nur: 35" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan", note: "Ustaz H. Abdurrahman Hasyim" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa daun zaitun: hijau perak, krem linen, dan ungu buah zaitun.", colors: ["#ece6d8", "#a8b4a0", "#5d6d4f", "#4a3446"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar Dr. Ir. Hasan Basri", "Keluarga Kajian Masjid Kampus"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, walimah menggunakan ruang terpisah dengan sekat untuk tamu putra dan putri." },
      { q: "Apakah tersedia tempat salat?", a: "Tersedia musala dan tempat wudu di sayap timur gedung." },
    ] },
  },
});
