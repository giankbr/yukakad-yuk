import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahira", groom: "Fathan",
    brideFull: "Zahira Hasna Mufidah, S.Si.", groomFull: "Fathan Ihsanul Haq, Lc.",
    brideParents: "Putri pertama dari\nBapak H. Muhammad Zuhri & Ibu Hj. Siti Khoiriyah",
    groomParents: "Putra kedua dari\nBapak K.H. Abdul Mughni & Ibu Nyai Hj. Umi Salamah",
    note: "Semoga Allah menumbuhkan cinta kami dengan tenang, sederhana, dan tetap harum seperti anyelir di pagi hari.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-11-06T08:00:00+07:00",
  place: "Masjid Jogokariyan",
  address: "Jl. Jogokaryan No. 36, Mantrijeron, Kota Yogyakarta",
  stories: [
    { date: "2023", title: "Kajian Pekanan", body: "Kami sama-sama menjadi panitia kajian remaja masjid, bertukar kabar hanya seperlunya." },
    { date: "2026", title: "Ta'aruf", body: "Melalui guru ngaji keluarga, kami bertukar biodata dan bertemu didampingi wali." },
    { date: "Agustus 2027", title: "Khitbah", body: "Keluarga Fathan datang bersilaturahmi, dan dengan izin Allah lamaran diterima." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-11-06T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jogokariyan", address: "Jl. Jogokaryan No. 36, Mantrijeron, Kota Yogyakarta" },
    { name: "Walimah", date: "2027-11-06T10:30:00+07:00", time: "10.30 – 13.00 WIB", venue: "Pendopo Omah Sekar", address: "Jl. Kaliurang Km 9,5, Sinduharjo, Ngaglik, Sleman" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 0213 46", account_name: "Zahira Hasna Mufidah" },
    { id: "demo-address", type: "address", address: "Jl. Parangtritis Km 3 No. 17, Sewon, Bantul, DI Yogyakarta 55187", account_name: "Keluarga H. Muhammad Zuhri" },
  ],
  guestName: "Ibu Hj. Aminah Zubaidah & Keluarga",
  guestTable: "Meja Melati 1",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "10.30", title: "Walimah", note: "Tamu putra & putri dipisah" },
      { time: "12.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim syar'i yang longgar. Nuansa mauve, krem, dan hijau sage dipersilakan.", colors: ["#b88aa6", "#f7f1e8", "#9aab95", "#4a3843"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Muhammad Zuhri", "Kel. Besar K.H. Abdul Mughni"] },
  },
});
