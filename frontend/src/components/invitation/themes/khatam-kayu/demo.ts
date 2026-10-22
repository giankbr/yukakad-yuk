import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Rayyan",
    brideFull: "Zahra Kamila Firdausi, S.Sn.", groomFull: "Rayyan Al Farisi, M.Ars.",
    brideParents: "Putri pertama dari\nBapak Dr. H. Faisal Rahman & Ibu Hj. Siti Maryam",
    groomParents: "Putra kedua dari\nBapak H. Ahmad Syarif Hidayat & Ibu Hj. Laila Nurhasanah",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Ribuan potongan kecil kayu, tulang, dan kuningan baru menjadi bintang bila disusun dengan sabar. Begitu pula kami, sepotong demi sepotong.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-24T11:00:00+07:00",
  place: "Rumah Kayu Jati",
  address: "Jl. Kemang Selatan Raya No. 88, Mampang Prapatan, Jakarta Selatan",
  stories: [
    { date: "2021", title: "Lokakarya Ukir Jepara", body: "Zahra datang untuk meneliti ragam hias, Rayyan untuk belajar menyambung kayu. Kami berbagi meja kerja dan satu kotak amplas." },
    { date: "2024", title: "Ta'aruf", body: "Setelah bertahun berteman dan berdiskusi tentang rumah impian, kami memutuskan saling mengenal dengan niat baik bersama keluarga." },
    { date: "Januari 2027", title: "Khitbah", body: "Keluarga Rayyan datang membawa sebuah kotak kayu bertatah buatan tangannya sendiri. Lamaran diterima dengan haru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-24T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Hikmah Kemang", address: "Jl. Bangka Raya No. 12, Mampang Prapatan, Jakarta Selatan" },
    { name: "Resepsi", date: "2027-04-24T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Kayu Jati", address: "Jl. Kemang Selatan Raya No. 88, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r43.webp", "/themes/img/r86.webp", "/themes/img/a124.webp", "/themes/img/a23.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7301 5528 60", account_name: "Zahra Kamila Firdausi" },
    { id: "demo-muamalat", type: "bank", bank_name: "Bank Muamalat", account_number: "3410 0277 15", account_name: "Rayyan Al Farisi" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka XI No. 3B, Pela Mampang, Jakarta Selatan 12720", account_name: "Keluarga Dr. H. Faisal Rahman" },
  ],
  guestName: "Ibu Hj. Nurhayati & Keluarga",
  guestTable: "Meja Kenari 6",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Teh rempah & kurma" },
      { time: "11.30", title: "Tilawah & doa" },
      { time: "12.00", title: "Santap siang", note: "Nasi kebuli & kebab" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim bernuansa kayu: cokelat walnut, gading, dan sentuhan kuningan.", colors: ["#5c3620", "#efe4cc", "#c9a253", "#2e1b0f"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Dr. H. Faisal Rahman", "Kel. Besar H. Ahmad Syarif Hidayat"] },
  },
});
