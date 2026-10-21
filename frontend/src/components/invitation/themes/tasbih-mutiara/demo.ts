import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Rayyan",
    brideFull: "Nadhira Salsabila, S.Farm.", groomFull: "Muhammad Rayyan Al-Fatih, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Zainal Abidin & Ibu Hj. Ummu Kultsum", groomParents: "Putra sulung dari\nBapak Drs. H. Fadhil Hasyim & Ibu Hj. Nur Aini",
    note: "Seperti butir tasbih yang dirangkai satu benang, semoga dua hati ini terikat dalam zikir dan sabar.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-12T08:00:00+07:00",
  place: "Masjid Raya Al-Falah",
  address: "Jl. Darmo No. 137, Darmo, Wonokromo, Surabaya",
  stories: [
    { date: "2024", title: "Ta'aruf", body: "Dipertemukan lewat guru ngaji kami, dengan niat yang sama: menjaga diri dan menyempurnakan separuh agama." },
    { date: "2026", title: "Khitbah", body: "Rayyan datang bersama keluarga meminang Nadhira, disambut doa dan senyum kedua orang tua." },
    { date: "2027", title: "Akad", body: "Insyaallah kami menyatukan niat dalam ikatan yang diridai-Nya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Al-Falah", address: "Jl. Darmo No. 137, Darmo, Wonokromo, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Sakinah Al-Falah", address: "Jl. Raya Darmo No. 139, Wonokromo, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7213 5566 0912", account_name: "Nadhira Salsabila" },
    { id: "demo-kado", type: "address", address: "Jl. Ketintang Baru IV No. 21, Gayungan, Surabaya 60231" },
  ],
  guestName: "Ibu Hj. Rahmawati & Keluarga",
  guestTable: "Meja Mutiara 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "08.45", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Tamu putra & putri terpisah" },
      { time: "12.15", title: "Doa bersama" },
    ] },
    dressCode: { note: "Busana muslim santun. Nuansa putih gading, sage, dan abu lembut.", colors: ["#f4f0e6", "#a7b89c", "#6d8670", "#c9c2b8"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zainal Abidin", "Kel. Besar Drs. H. Fadhil Hasyim"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, walimah menggunakan ruang terpisah untuk tamu putra dan putri." },
      { q: "Apakah tersedia musala?", a: "Tersedia di lantai dasar Graha Sakinah, lengkap dengan tempat wudu." },
    ] },
  },
});
