import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Safiya", groom: "Ilham",
    brideFull: "Safiya Nur Azizah, S.Hum.", groomFull: "Ilham Ramadhan Hakim, M.Sc.",
    brideParents: "Putri pertama dari\nBapak H. Ahmad Zakaria & Ibu Hj. Nurul Hidayah", groomParents: "Putra ketiga dari\nBapak Drs. Lukman Hakim & Ibu Siti Rahmawati",
    note: "Tiga titik dan dua gelombang: semoga cinta kami tenang, kuat, dan senantiasa dalam lindungan-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-12T08:00:00+07:00",
  place: "Aula Kencana Graha",
  address: "Jl. Ir. H. Juanda No. 88, Dago, Coblong, Kota Bandung",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2021", title: "Ruang Baca Naskah", body: "Safiya meneliti kain-kain Utsmani untuk skripsinya, Ilham membantu memotret koleksi museum. Kami berkenalan di antara lembar-lembar katalog." },
    { date: "2025", title: "Khitbah", body: "Keluarga Ilham bersilaturahmi ke rumah di Cimahi, membawa niat baik dan sebakul doa." },
    { date: "2027", title: "Akad", body: "Dengan izin Allah dan restu kedua orang tua, kami menyempurnakan separuh agama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimah", date: "2027-09-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Kencana Graha", address: "Jl. Ir. H. Juanda No. 88, Dago, Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a123.webp", "/themes/img/a110.webp", "/themes/img/a131.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7211 0908 12", account_name: "Safiya Nur Azizah" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "130 00 1234567 8", account_name: "Ilham Ramadhan Hakim" },
  ],
  guestName: "Ibu Dr. Laila Fitriani & Keluarga",
  guestTable: "Meja Kemha 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    dressCode: { note: "Busana muslim formal. Merah delima, gading, dan emas dipersilakan.", colors: ["#9e1427", "#f3e8d2", "#c49a3e", "#4a0711"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-12T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Zakaria", "Kel. Besar Drs. Lukman Hakim"] },
  },
});
