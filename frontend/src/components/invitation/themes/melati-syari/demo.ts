import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hanifah", groom: "Zaki",
    brideFull: "Hanifah Nur Azizah, S.Pd.", groomFull: "Muhammad Zaki Ramadhan, S.Kom.",
    brideParents: "Putri sulung dari\nBapak H. Dadang Kurniawan & Ibu Hj. Euis Sumiati", groomParents: "Putra ketiga dari\nBapak H. Asep Saepudin & Ibu Hj. Neneng Rohimah",
    note: "Seperti melati yang dironce satu per satu, semoga setiap hari kami dirangkai dengan sabar, syukur, dan doa.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-24T08:00:00+07:00",
  place: "Masjid Al-Irsyad Satya",
  address: "Kota Baru Parahyangan, Padalarang, Kabupaten Bandung Barat",
  stories: [
    { date: "2023", title: "Satu Majelis", body: "Kami sama-sama menjadi pengajar di rumah tahfiz di Cimahi, saling mengenal hanya lewat jadwal mengajar." },
    { date: "2025", title: "Ta'aruf", body: "Melalui ustazah pembimbing, kami bertukar biodata dan berproses dengan didampingi keluarga." },
    { date: "Januari 2027", title: "Khitbah", body: "Keluarga Zaki datang ke Lembang membawa seserahan dan ronce melati; lamaran diterima dengan haru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-24T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Irsyad Satya", address: "Kota Baru Parahyangan, Padalarang, Kabupaten Bandung Barat" },
    { name: "Walimatul 'Ursy", date: "2027-04-24T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7180 3322 4561", account_name: "Hanifah Nur Azizah" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3310 0447 82", account_name: "Muhammad Zaki Ramadhan" },
    { id: "demo-kado", type: "address", address: "Jl. Kolonel Masturi No. 88, Lembang, Kabupaten Bandung Barat 40391", account_name: "Keluarga H. Dadang Kurniawan" },
  ],
  guestName: "Ibu Hj. Siti Maryam & Keluarga",
  guestTable: "Meja Melati 2",
  extras: {
    quote: { text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu. Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya.", source: "QS. An-Nur: 32" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa segar: putih melati, hijau daun, dan krem.", colors: ["#fbfbf4", "#9cc489", "#4f8a4c", "#efe4c4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dadang Kurniawan", "Kel. Besar H. Asep Saepudin"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, walimah menggunakan ruang terpisah untuk tamu putra dan putri." },
      { q: "Apakah ada tempat salat?", a: "Tersedia musala dan tempat wudu di lantai dasar gedung Pusdai." },
    ] },
  },
});
