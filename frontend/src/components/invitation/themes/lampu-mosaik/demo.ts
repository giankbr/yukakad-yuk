import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Raihan",
    brideFull: "Nadia Khairunnisa, S.Ds.", groomFull: "Muhammad Raihan Al-Fatih, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Syarifuddin & Ibu Hj. Nurul Aini",
    groomParents: "Putra pertama dari\nBapak Ir. H. Fauzan Hakim & Ibu Hj. Laila Fitriani",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti kepingan kaca kecil yang disusun dengan sabar, kami ingin saling melengkapi hingga menjadi satu cahaya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T19:00:00+07:00",
  place: "Hotel Borobudur Jakarta",
  address: "Jl. Lapangan Banteng Selatan No. 1, Sawah Besar, Jakarta Pusat",
  stories: [
    { date: "2022", title: "Bazar Ramadan", body: "Kami bertemu di antara deretan lampu kaca di bazar Ramadan, sama-sama menawar lampu yang sama." },
    { date: "2025", title: "Ta'aruf", body: "Lewat sahabat kampus, kami saling mengenal dengan niat baik dan didampingi keluarga." },
    { date: "Maret 2027", title: "Khitbah", body: "Selepas tarawih, keluarga Raihan datang bersilaturahmi dan lamaran diterima dengan haru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T16:00:00+07:00", time: "16.00 – 17.30 WIB", venue: "Masjid Istiqlal", address: "Jl. Taman Wijaya Kusuma, Ps. Baru, Sawah Besar, Jakarta Pusat" },
    { name: "Resepsi", date: "2027-10-16T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Hotel Borobudur Jakarta, Flores Ballroom", address: "Jl. Lapangan Banteng Selatan No. 1, Sawah Besar, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/r63.webp", "/themes/img/a101.webp", "/themes/img/r64.webp", "/themes/img/a123.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 4459 18", account_name: "Nadia Khairunnisa" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1240 0098 7765", account_name: "Muhammad Raihan Al-Fatih" },
    { id: "demo-kado", type: "address", address: "Jl. Cikini Raya No. 58, Menteng, Jakarta Pusat 10330", account_name: "Keluarga H. Ahmad Syarifuddin" },
  ],
  guestName: "Bapak H. Lukman Hakim & Keluarga",
  guestTable: "Meja Firuze 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.00", title: "Penyambutan tamu", note: "Lorong lampu kaca" },
      { time: "19.30", title: "Kirab mempelai & doa" },
      { time: "20.00", title: "Santap malam & gambus" },
      { time: "21.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim formal bernuansa permata: merah delima, biru pirus, kuning kunyit, atau ungu.", colors: ["#b8203a", "#1f8f9a", "#e08a26", "#6a34a0"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T16:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar Ir. H. Fauzan Hakim"] },
  },
});
