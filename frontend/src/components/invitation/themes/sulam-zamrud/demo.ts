import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Ilham",
    brideFull: "Aisyah Nur Rahmah, S.Pd.I.", groomFull: "Ilham Maulana Hakim, Lc.",
    brideParents: "Putri pertama dari\nBapak K.H. Abdurrahman & Ibu Hj. Siti Mariyam", groomParents: "Putra kedua dari\nBapak H. Zainal Arifin & Ibu Hj. Umi Kultsum",
    note: "Semoga Allah menjadikan rumah kami tempat yang tenang, dijahit dengan sabar dan syukur.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-03-20T08:00:00+07:00",
  place: "Pendopo Agung Royal Ambarrukmo",
  address: "Jl. Laksda Adisucipto No. 81, Caturtunggal, Depok, Sleman, Yogyakarta",
  stories: [
    { date: "2025", title: "Ta'aruf", body: "Dikenalkan oleh guru mengaji kami, saling bertukar biodata dan doa." },
    { date: "2026", title: "Khitbah", body: "Keluarga Ilham datang ke Yogyakarta, disambut hangat oleh keluarga Aisyah." },
    { date: "2027", title: "Akad", body: "Dengan bismillah, kami memulai ibadah terpanjang." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-20T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Gedhe Kauman", address: "Jl. Kauman, Ngupasan, Gondomanan, Kota Yogyakarta" },
    { name: "Walimatul 'Ursy", date: "2027-03-20T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Pendopo Agung Royal Ambarrukmo", address: "Jl. Laksda Adisucipto No. 81, Caturtunggal, Depok, Sleman, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7311 0098 24", account_name: "Aisyah Nur Rahmah" },
    { id: "demo-kado", type: "address", address: "Jl. Kaliurang Km 7, Gg. Pandega Marta No. 4, Sleman, Yogyakarta 55581" },
  ],
  guestName: "Bapak Ustadz Hasan & Keluarga",
  guestTable: "Meja Zamrud 2",
  extras: {
    quote: { text: "Dan Kami ciptakan kamu berpasang-pasangan.", source: "QS. An-Naba': 8" },
    rundown: { items: [
      { time: "11.00", title: "Pembukaan & tilawah" },
      { time: "11.20", title: "Tausiyah pernikahan", note: "Ustadz Ahmad Fauzi" },
      { time: "12.00", title: "Ramah tamah", note: "Tamu putra & putri terpisah" },
    ] },
    dressCode: { note: "Busana muslim yang sopan. Hijau dan krem dipersilakan.", colors: ["#0f5b44", "#d9b75e", "#f4ecd6", "#ebbfae"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar K.H. Abdurrahman", "Kel. Besar H. Zainal Arifin"] },
  },
});
