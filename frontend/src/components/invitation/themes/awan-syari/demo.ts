import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nabila", groom: "Fathan",
    brideFull: "Nabila Khairunnisa, S.Psi.", groomFull: "Muhammad Fathan Alfarizi, S.Kom.",
    brideParents: "Putri pertama dari\nBapak H. Ridwan Saputra & Ibu Hj. Nur Aisyah", groomParents: "Putra kedua dari\nBapak Ahmad Syarifuddin & Ibu Siti Rahmawati",
    note: "Semoga Allah menghimpun yang terserak dari keduanya, memberkahi mereka, dan mengumpulkan keduanya dalam kebaikan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Nurul Falah",
  address: "Jl. Cigadung Raya Timur No. 8, Cibeunying Kaler, Kota Bandung, Jawa Barat",
  stories: [
    { date: "2024", title: "Bertemu di Kajian Pekanan", body: "Kami sama-sama menjadi panitia kajian remaja masjid. Tidak banyak bicara, hanya saling menghormati dari kejauhan." },
    { date: "2026", title: "Ta'aruf", body: "Melalui perantara ustazah dan keluarga, kami bertukar biodata, lalu bertemu didampingi keluarga untuk saling mengenal." },
    { date: "2027", title: "Khitbah & Menuju Akad", body: "Alhamdulillah, keluarga Fathan datang mengkhitbah. Dengan restu kedua orang tua, kami menetapkan hari akad." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Nurul Falah", address: "Jl. Cigadung Raya Timur No. 8, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Bale Asri", address: "Jl. Dago Giri No. 21, Mekarwangi, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 3398 41", account_name: "Nabila Khairunnisa" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3040 0187 22", account_name: "Muhammad Fathan Alfarizi" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Timur No. 14, Cibeunying Kaler, Kota Bandung 40191" },
  ],
  guestName: "Ibu Hj. Fitriani & Keluarga",
  guestTable: "Meja Awan 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Tamu putra dan putri di ruang terpisah" },
      { time: "11.30", title: "Tausiyah pernikahan" },
      { time: "12.00", title: "Ishoma & jamuan" },
      { time: "13.00", title: "Doa bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Nuansa biru langit, putih, dan krem.", colors: ["#cfe2f1", "#ffffff", "#f3e2c8", "#2f5476"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ridwan Saputra", "Kel. Besar Ahmad Syarifuddin"] },
    faq: { items: [
      { q: "Apakah tempat duduk tamu dipisah?", a: "Ya, area tamu putra dan putri dipisah dengan tabir agar semua tamu nyaman." },
      { q: "Apakah tersedia musala?", a: "Tersedia musala dan tempat wudu di sisi kanan aula." },
    ] },
  },
});
