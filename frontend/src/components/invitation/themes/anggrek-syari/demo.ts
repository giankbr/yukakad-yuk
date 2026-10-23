import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nabila", groom: "Hanif",
    brideFull: "Nabila Azzahra Puspitasari", groomFull: "Hanif Abdurrahman Siregar, S.Pd.",
    brideParents: "Putri pertama dari\nBapak H. Dedi Supriatna & Ibu Hj. Ratna Komalasari", groomParents: "Putra kedua dari\nBapak H. Mulia Siregar & Ibu Hj. Siti Hajar Nasution",
    note: "Semoga cinta kami tumbuh seperti anggrek bulan: tenang, bersih, dan setia mekar pada musimnya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-19T09:00:00+07:00",
  place: "Gedung Serbaguna Pusdai",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung",
  stories: [
    { date: "2022", title: "Majelis Ilmu", body: "Kami pertama kali saling mengenal nama lewat panitia kajian remaja masjid di Bandung, tanpa banyak kata." },
    { date: "2026", title: "Ta'aruf", body: "Dengan perantara guru ngaji kami, Hanif menyampaikan niat baiknya. Kami bertukar biodata dan saling mendoakan." },
    { date: "2027", title: "Akad", body: "Setelah khitbah yang hangat bersama dua keluarga, insyaallah kami melangsungkan akad nikah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.00 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimah", date: "2027-06-19T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Gedung Serbaguna Pusdai", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 2041 63", account_name: "Nabila Azzahra Puspitasari" },
    { id: "demo-bjb", type: "bank", bank_name: "BJB Syariah", account_number: "5130 2088 1172", account_name: "Hanif Abdurrahman Siregar" },
    { id: "demo-kado", type: "address", address: "Jl. Sukaluyu No. 27, Cibeunying Kaler, Kota Bandung 40123" },
  ],
  guestName: "Ibu Hj. Euis Sumiati & Keluarga",
  guestTable: "Meja Anggrek 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "10.00", title: "Pembukaan & tilawah" },
      { time: "10.20", title: "Tausiyah pernikahan", note: "Ustadz H. Ahmad Fauzi" },
      { time: "10.50", title: "Doa & ramah tamah", note: "Tamu putra dan putri terpisah" },
    ] },
    dressCode: { note: "Busana muslim/muslimah yang longgar dan sopan. Putih, ungu muda, dan krem dipersilakan.", colors: ["#fbf7f0", "#c9a6d8", "#7b3f8c", "#e8dfcf"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dedi Supriatna", "Kel. Besar H. Mulia Siregar"] },
  },
});
