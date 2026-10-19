import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Arkan",
    note: "Satu janji kecil di jari manis, satu langkah besar menuju halal.",
    brideFull: "Nadhira Salsabila Azzahra, S.Farm.", groomFull: "Arkan Maulana Ibrahim, S.Kom.",
    brideParents: "Putri pertama dari\nBapak Hendra Gunawan & Ibu Fitri Handayani", groomParents: "Putra kedua dari\nBapak Ahmad Fauzi & Ibu Rahmawati",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
  },
  eventLabel: "Lamaran",
  date: "2027-03-20T10:00:00+07:00",
  place: "Kediaman Keluarga Bapak Hendra Gunawan",
  address: "Jl. Cigadung Raya Barat No. 18, Cibeunying Kaler, Bandung",
  stories: [
    { date: "2021", title: "Kenal lewat kajian", body: "Bertemu di sebuah kajian pekanan di Bandung. Sapa singkat yang kemudian berlanjut menjadi diskusi panjang." },
    { date: "2025", title: "Taaruf", body: "Dengan restu kedua keluarga, kami memulai taaruf dan belajar saling memahami." },
    { date: "2027", title: "Khitbah", body: "Kini keluarga Arkan datang untuk meminang secara resmi, ditandai dengan cincin pengikat." },
  ],
  events: [
    { name: "Prosesi Lamaran", date: "2027-03-20T10:00:00+07:00", time: "10.00 – 11.00 WIB", venue: "Kediaman Keluarga Bapak Hendra Gunawan", address: "Jl. Cigadung Raya Barat No. 18, Cibeunying Kaler, Bandung" },
    { name: "Tukar Cincin & Ramah Tamah", date: "2027-03-20T11:00:00+07:00", time: "11.00 – 13.00 WIB", venue: "Taman Belakang Kediaman", address: "Jl. Cigadung Raya Barat No. 18, Cibeunying Kaler, Bandung" },
  ],
  gallery: ["/themes/img/r84.webp", "/themes/img/r5.webp", "/themes/img/a26.webp", "/themes/img/r13.webp", "/themes/img/r65.webp", "/themes/img/a85.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7211 4590 88", account_name: "Nadhira Salsabila Azzahra" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0813 2244 6688", account_name: "Arkan Maulana" },
  ],
  guestName: "Ibu Dewi Sartika & Keluarga",
  extras: {
    quote: { text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu, dan juga orang-orang yang layak dari hamba-hamba sahayamu.", source: "QS. An-Nur: 32" },
    rundown: { items: [
      { time: "10.00", title: "Penyambutan keluarga Arkan" },
      { time: "10.20", title: "Penyampaian maksud & jawaban lamaran", note: "Juru bicara kedua keluarga" },
      { time: "11.00", title: "Tukar cincin", note: "Disematkan oleh ibunda kedua mempelai" },
      { time: "11.30", title: "Doa & ramah tamah" },
    ] },
    dressCode: { note: "Nuansa champagne, krem, dan nude. Busana muslim dipersilakan.", colors: ["#e9d8bf", "#f6efe6", "#c89b8f", "#b8955a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak Hendra Gunawan", "Kel. Besar Bapak Ahmad Fauzi"] },
    faq: { items: [
      { q: "Apakah acara terbuka untuk umum?", a: "Acara ini khusus untuk keluarga dan kerabat dekat yang menerima undangan." },
      { q: "Di mana tamu bisa parkir?", a: "Parkir tersedia di halaman Masjid Al-Ikhlas, 100 m dari kediaman." },
    ] },
  },
});
