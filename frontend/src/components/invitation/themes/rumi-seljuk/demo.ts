import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kamila", groom: "Faruq",
    brideFull: "Kamila Azzahra Putri, S.Ars.", groomFull: "Muhammad Faruq Al-Hakim, S.T.",
    brideParents: "Putri pertama dari\nBapak H. Arif Budiman & Ibu Hj. Ratna Kurniawati", groomParents: "Putra kedua dari\nBapak Drs. Syamsul Bahri & Ibu Nurlela",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti ubin yang saling mengunci, kami ingin saling melengkapi.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-09T08:00:00+07:00",
  place: "Balai Kartini",
  address: "Jl. Gatot Subroto Kav. 37, Kuningan Timur, Setiabudi, Jakarta Selatan",
  stories: [
    { date: "2021", title: "Kuliah Lapangan", body: "Kami bertemu di kuliah lapangan arsitektur Islam, sama-sama sibuk menggambar sulur ubin di sebuah masjid tua." },
    { date: "2024", title: "Taaruf", body: "Lewat perantara guru mengaji, kami berkenalan dengan niat baik dan saling mengenal keluarga masing-masing." },
    { date: "2026", title: "Khitbah", body: "Keluarga Faruq datang meminang dengan sederhana. Bismillah, kami memantapkan langkah menuju akad." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Ikhlas", address: "Jl. Cipete Raya No. 9, Cipete Selatan, Cilandak, Jakarta Selatan" },
    { name: "Walimatul 'Ursy", date: "2027-10-09T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Kartini", address: "Jl. Gatot Subroto Kav. 37, Kuningan Timur, Setiabudi, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/r57.webp", "/themes/img/r58.webp", "/themes/img/a49.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2288 51", account_name: "Kamila Azzahra Putri" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3310 0047 82", account_name: "Muhammad Faruq Al-Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Fatmawati Raya No. 18, Cilandak Barat, Jakarta Selatan" },
  ],
  guestName: "Bapak H. Zainal Abidin & Keluarga",
  guestTable: "Meja Pirus 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "08.20", title: "Ijab kabul", note: "Keluarga inti & saksi" },
      { time: "11.00", title: "Walimah dibuka" },
      { time: "12.00", title: "Doa bersama & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim bernuansa pirus, biru kobalt, atau krem batu.", colors: ["#2f9e9a", "#1f3c8c", "#e7dcc4", "#2b2233"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Arif Budiman", "Kel. Besar Drs. Syamsul Bahri", "Ikatan Alumni Arsitektur 2017"] },
  },
});
