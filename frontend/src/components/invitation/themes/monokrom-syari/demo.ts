import { makeDemo } from "../demo-base";

// Syari tanpa foto: akad di masjid dan walimah sederhana di aula yang sama, tamu pria dan wanita terpisah.
export const demo = makeDemo({
  couple: {
    bride: "Nabila", groom: "Faris",
    brideFull: "Nabila Khairunnisa, S.Pd.", groomFull: "Muhammad Faris Hamdani, S.T.",
    brideParents: "Putri ketiga dari\nBapak H. Ridwan Syarifudin & Ibu Hj. Euis Rahmawati", groomParents: "Putra pertama dari\nBapak Drs. Hamdan Fauzi & Ibu Siti Mardiyah",
    note: "Hitam dan putih, garis dan ruang: semoga rumah tangga kami sederhana dalam rupa dan jelas dalam arah, menuju ridha-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-09T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Bandung",
  stories: [
    { date: "2024", title: "Ta'aruf", body: "Dipertemukan lewat kajian pekanan dan dikenalkan oleh ustadzah keluarga, kami bertukar biodata dengan didampingi orang tua." },
    { date: "2026", title: "Khitbah", body: "Keluarga Faris datang meminang dengan niat baik. Istikharah kedua keluarga berujung pada jawaban yang menenangkan." },
    { date: "2027", title: "Akad", body: "Insyaallah kami menyempurnakan separuh agama. Mohon doa agar langkah ini diberkahi dari awal hingga akhir." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-10-09T10:30:00+07:00", time: "10.30 – 13.00 WIB", venue: "Aula Pusdai", address: "Kompleks Masjid Pusdai, Jl. Diponegoro No. 63, Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 0927 31", account_name: "Nabila Khairunnisa" },
    { id: "demo-kado", type: "address", address: "Jl. Sukaluyu No. 27, Cibeunying Kaler, Bandung 40123" },
  ],
  guestName: "Ibu Hj. Ratna & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "10.30", title: "Pembukaan & tilawah" },
      { time: "10.50", title: "Tausiyah pernikahan", note: "Ustadz Hanif Abdurrahman" },
      { time: "11.30", title: "Ramah tamah", note: "Area tamu pria dan wanita terpisah" },
    ] },
    dressCode: { note: "Busana muslim sopan dalam nuansa hitam, putih, atau abu-abu.", colors: ["#111111", "#ffffff", "#8a8a8a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ridwan Syarifudin", "Kel. Besar Drs. Hamdan Fauzi"] },
  },
});
