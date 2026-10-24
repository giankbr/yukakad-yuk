import { makeDemo } from "../demo-base";

// Walimah di Surabaya: keluarga pedagang attar di Kampung Arab Ampel, botol kaca berwarna, dan harum gaharu.
export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Rayyan",
    brideFull: "Aisyah Nur Fadhilah, S.Farm.", groomFull: "Rayyan Abdullah Al Habsyi, S.E.",
    brideParents: "Putri pertama dari\nBapak H. Umar Bahasuan & Ibu Hj. Fatimah Assegaf", groomParents: "Putra ketiga dari\nBapak H. Abdullah Al Habsyi & Ibu Hj. Khadijah Baraja",
    note: "Wangi yang baik tidak berteriak; ia tinggal lama di ingatan. Semoga begitu pula rumah tangga kami.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T08:00:00+07:00",
  place: "Hotel Majapahit Surabaya",
  address: "Jl. Tunjungan No. 65, Genteng, Kota Surabaya, Jawa Timur",
  stories: [
    { date: "2022", title: "Sebotol Kecil Kasturi", body: "Aisyah mampir ke toko attar keluarga Rayyan di Ampel untuk membeli hadiah umrah bagi ibunya. Rayyan meraciknya sendiri, lalu lupa menagih." },
    { date: "2025", title: "Racikan yang Pas", body: "Kami belajar bahwa wangi terbaik lahir dari kesabaran: gaharu yang didiamkan, mawar Taif yang disuling pelan. Begitu juga kami saling mengenal." },
    { date: "2027", title: "Satu Botol, Dua Nama", body: "Dengan restu kedua keluarga, kami meracik satu attar untuk hari bahagia, dan kami ingin Bapak/Ibu turut menciumnya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sunan Ampel", address: "Jl. Petukangan I, Ampel, Kec. Semampir, Kota Surabaya" },
    { name: "Walimah", date: "2027-10-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Hotel Majapahit Surabaya", address: "Jl. Tunjungan No. 65, Genteng, Kota Surabaya" },
  ],
  gallery: ["/themes/img/a99.webp", "/themes/img/a26.webp", "/themes/img/r57.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 1610 2027", account_name: "Aisyah Nur Fadhilah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7331 1027 40", account_name: "Rayyan Abdullah Al Habsyi" },
    { id: "demo-kado", type: "address", address: "Jl. Ampel Suci No. 31, Ampel, Kec. Semampir, Kota Surabaya 60151" },
  ],
  guestName: "Bapak H. Salim Bawazier & Keluarga",
  guestTable: "Meja Oud 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Diiringi gambus dan hadrah" },
      { time: "11.30", title: "Doa & tausiyah singkat" },
      { time: "12.00", title: "Jamuan walimah", note: "Nasi kebuli, gulai kambing, dan teh susu" },
    ] },
    dressCode: { note: "Busana muslim bernuansa permata: zamrud, delima, nila, atau emas.", colors: ["#1f7a5a", "#a8243a", "#2a4ea0", "#c9a052", "#3a1530"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak H. Umar Bahasuan", "Kel. Besar Bapak H. Abdullah Al Habsyi"] },
  },
});
