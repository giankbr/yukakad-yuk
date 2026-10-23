import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Hanif",
    brideFull: "Salma Nur Azizah, S.Farm.", groomFull: "Muhammad Hanif Alfarisi, Lc.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Syarifuddin & Ibu Hj. Nurul Hidayah",
    groomParents: "Putra sulung dari\nBapak Drs. Abdul Karim & Ibu Siti Maryam",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti delima yang menyimpan ratusan biji dalam satu kulit, semoga cinta kami menghimpun banyak keberkahan dalam satu rumah.",
  },
  eventLabel: "Walimatul 'Urs",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung",
  stories: [
    { date: "2021", title: "Majelis Ilmu", body: "Kami pertama kali bertemu di kajian pekanan di masjid kampus. Salma menjadi panitia, Hanif mengisi tilawah pembuka." },
    { date: "2025", title: "Ta'aruf", body: "Lewat perantara guru ngaji kami, dua keluarga saling mengenal. Kami bertukar cerita tentang cita-cita dan arah hidup." },
    { date: "2026", title: "Khitbah", body: "Keluarga Hanif datang melamar di bulan Syawal. Bismillah, kami mantap melangkah bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung" },
    { name: "Walimah", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Serbaguna Pusdai", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung" },
  ],
  gallery: ["/themes/img/r3.webp", "/themes/img/r57.webp", "/themes/img/r4.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Salma Nur Azizah" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0217 4455 6", account_name: "Muhammad Hanif Alfarisi" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Barat No. 12, Kec. Cibeunying Kaler, Kota Bandung 40191" },
  ],
  guestName: "Ibu Hj. Fatimah Az-Zahra & Keluarga",
  guestTable: "Meja Delima 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "08.20", title: "Ijab kabul", note: "Disaksikan keluarga dan para undangan" },
      { time: "09.00", title: "Khutbah nikah & doa" },
      { time: "11.00", title: "Walimah & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim rapi dan santun. Nuansa merah delima, krem, dan hijau daun dipersilakan.", colors: ["#8e1b24", "#f6eddb", "#4d6b3a", "#c69a45"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar Drs. Abdul Karim"] },
    faq: { items: [
      { q: "Apakah tempat akad dan walimah sama?", a: "Ya, keduanya di kompleks Pusdai. Walimah berlangsung di aula serbaguna." },
      { q: "Apakah tersedia tempat salat?", a: "Tersedia, masjid utama terbuka untuk tamu sepanjang acara." },
    ] },
  },
});
