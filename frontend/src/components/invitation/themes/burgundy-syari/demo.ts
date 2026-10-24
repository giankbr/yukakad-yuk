import { makeDemo } from "../demo-base";

// Walimah syar'i tanpa foto: burgundy anggur, beludru, emas, dan bunga kering. Bandung, akhir musim hujan.
export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Faris",
    brideFull: "Nadhira Salsabila Rahman", groomFull: "Muhammad Faris Al-Hakim",
    brideParents: "Putri ketiga dari\nBapak H. Abdurrahman Saleh & Ibu Hj. Rahmawati", groomParents: "Putra pertama dari\nBapak Ir. H. Hakim Nurdin & Ibu Hj. Siti Khadijah",
    note: "Semoga Allah menghimpun yang dua dalam kebaikan, dan menjadikan rumah kecil kami tempat yang hangat untuk pulang.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-03-13T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung",
  stories: [
    { date: "Syawal 1447 H", title: "Ta'aruf", body: "Dipertemukan lewat guru mengaji kami, dengan proposal yang ditulis tangan dan pertanyaan yang dijawab dengan jujur." },
    { date: "Rabiul Awal 1448 H", title: "Khitbah", body: "Keluarga Faris datang ke Bandung membawa seikat bunga kering dan niat yang sudah bulat." },
    { date: "Syawal 1448 H", title: "Menuju Akad", body: "Selepas Idulfitri, dengan restu kedua orang tua, kami menyempurnakan separuh agama dalam rahmat-Nya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-13T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-03-13T11:00:00+07:00", time: "11.00 – 14.00 WIB · tamu putra & putri terpisah", venue: "Aula Darussalam", address: "Jl. Cigadung Raya Timur No. 18, Kec. Cibeunying Kaler, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7213 5580 12", account_name: "Nadhira Salsabila Rahman" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3310 0047 21", account_name: "Muhammad Faris Al-Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Timur No. 18, Kota Bandung 40191" },
  ],
  guestName: "Ustadzah Fatimah Az-Zahra & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Pembukaan & tilawah" },
      { time: "11.20", title: "Tausiyah pernikahan", note: "Oleh Ustadz H. Ahmad Fauzi, Lc." },
      { time: "12.00", title: "Ramah tamah", note: "Tamu putra dan putri di ruang terpisah" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Burgundy, krem, dan emas lembut dipersilakan.", colors: ["#5c1626", "#8a2f40", "#efe2d4", "#c9a45a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdurrahman Saleh", "Kel. Besar Ir. H. Hakim Nurdin"] },
  },
});
