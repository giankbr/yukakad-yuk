import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Rizky",
    brideFull: "Nadia Putri Rahmadani, S.Farm.", groomFull: "Rizky Febrian Saputra, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Zulkarnain & Ibu Hj. Darmawati", groomParents: "Putra sulung dari\nBapak Syafriadi & Ibu Nurhayati",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Seperti rafflesia yang tumbuh perlahan di rimba Bengkulu lalu mekar sempurna, cinta kami dirawat dengan sabar hingga tiba waktunya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T08:30:00+07:00",
  place: "Balai Raya Semarak Bengkulu",
  address: "Jl. Pembangunan, Padang Harapan, Gading Cempaka, Kota Bengkulu",
  stories: [
    { date: "2019", title: "Benteng Marlborough", body: "Kami berkenalan saat menjadi pemandu sukarela tur sejarah kota. Rizky salah menyebut tahun berdirinya benteng, Nadia yang membetulkan." },
    { date: "2023", title: "Senja di Pantai Panjang", body: "Setiap Sabtu sore kami bersepeda di sepanjang pantai, berhenti untuk pendap dan teh hangat di bawah cemara." },
    { date: "2026", title: "Antar Tando", body: "Keluarga Rizky datang membawa tanda ikatan. Dua keluarga besar bermufakat menentukan hari baik di bulan Juni." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Raya Baitul Izzah", address: "Jl. Pembangunan, Padang Harapan, Gading Cempaka, Kota Bengkulu" },
    { name: "Resepsi", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Raya Semarak Bengkulu", address: "Jl. Pembangunan, Padang Harapan, Gading Cempaka, Kota Bengkulu" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r3.webp", "/themes/img/r26.webp", "/themes/img/r109.webp", "/themes/img/r6.webp", "/themes/img/a118.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7180 2233 41", account_name: "Nadia Putri Rahmadani" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0120 0109 4455 508", account_name: "Rizky Febrian Saputra" },
    { id: "demo-kado", type: "address", address: "Jl. Soekarno-Hatta No. 18, Anggut Atas, Ratu Samban, Kota Bengkulu 38222" },
  ],
  guestName: "Bapak H. Darwis & Keluarga",
  guestTable: "Meja Cempaka 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Diiringi dol dan rebana" },
      { time: "11.30", title: "Tari Andun & sambutan keluarga" },
      { time: "12.30", title: "Ramah tamah", note: "Pendap, lemang tapai, dan bagar" },
    ] },
    dressCode: { note: "Busana muslim atau batik besurek. Merah bata, hijau rimba, dan krem dipersilakan.", colors: ["#b9442b", "#2f5d3c", "#f1dfc4", "#e08a4f"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-19T08:30:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkarnain (Kota Bengkulu)", "Kel. Besar Syafriadi (Curup, Rejang Lebong)"] },
  },
});
