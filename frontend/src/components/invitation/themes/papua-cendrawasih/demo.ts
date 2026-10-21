import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Yuliana", groom: "Daniel",
    brideFull: "Yuliana Ohee, S.Pd.", groomFull: "Daniel Rumbiak, S.T.",
    brideParents: "Putri kedua dari\nBapak Yohanis Ohee & Ibu Martha Pepuho", groomParents: "Putra sulung dari\nBapak Markus Rumbiak & Ibu Selfina Mandowen",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Seperti noken yang dirajut simpul demi simpul, kasih kami dijalin dengan sabar dan dibawa bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T10:00:00+09:00",
  place: "Gedung Pertemuan Hinekombe",
  address: "Jl. Raya Sentani, Hinekombe, Sentani, Kabupaten Jayapura, Papua",
  stories: [
    { date: "2020", title: "Di Tepi Danau Sentani", body: "Kami bertemu saat sama-sama menjadi relawan Festival Danau Sentani, menata perahu-perahu hias di pagi berkabut." },
    { date: "2023", title: "Pulang ke Kampung", body: "Daniel datang bersama keluarga ke kampung Yuliana, membawa salam dan niat baik untuk saling mengenal lebih dekat." },
    { date: "2027", title: "Satu Noken, Satu Rumah", body: "Dengan restu orang tua dan berkat Tuhan, kami siap membangun rumah tangga di tanah Papua yang kami cintai." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-17T10:00:00+09:00", time: "10.00 – 11.30 WIT", venue: "Gereja GKI Bethel Sentani", address: "Jl. Kemiri Sentani, Sentani Kota, Kabupaten Jayapura" },
    { name: "Resepsi & Pesta Adat", date: "2027-07-17T17:00:00+09:00", time: "17.00 – 21.00 WIT", venue: "Gedung Pertemuan Hinekombe", address: "Jl. Raya Sentani, Hinekombe, Sentani, Kabupaten Jayapura" },
  ],
  gallery: ["/themes/img/r10.webp", "/themes/img/r110.webp", "/themes/img/r105.webp", "/themes/img/r29.webp", "/themes/img/r27.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Papua", account_number: "1501 0234 5678", account_name: "Yuliana Ohee" },
    { id: "demo-kado", type: "address", address: "Jl. Pasar Lama No. 8, Sentani Kota, Kabupaten Jayapura 99352" },
  ],
  guestName: "Bapak Lukas Wenda & Keluarga",
  guestTable: "Meja 7",
  extras: {
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Diiringi tifa & lagu daerah" },
      { time: "18.00", title: "Ibadah syukur & doa berkat" },
      { time: "19.00", title: "Makan bersama", note: "Papeda, ikan kuah kuning & bakar batu" },
      { time: "20.00", title: "Yospan bersama" },
    ] },
    dressCode: { note: "Nuansa tanah: merah bata, oker, hitam, dan krem. Motif Papua sangat dipersilakan.", colors: ["#9c3b1f", "#c98a2b", "#1d1410", "#f3e6cf"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-17T10:00:00+09:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ohee – Pepuho", "Kel. Besar Rumbiak – Mandowen", "Jemaat GKI Bethel Sentani"] },
  },
});
