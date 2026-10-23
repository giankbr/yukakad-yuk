import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alifa", groom: "Hanif",
    brideFull: "Alifa Nur Azizah, S.Pd.", groomFull: "Muhammad Hanif Ramadhan, S.T.",
    brideParents: "Putri pertama dari\nBapak H. Imam Syafi'i & Ibu Hj. Nur Laili", groomParents: "Putra kedua dari\nBapak Drs. Abdul Hakim & Ibu Siti Khoiriyah",
    note: "Semoga Allah menumbuhkan cinta kami seperti daun mint: sederhana, menyegarkan, dan membawa kebaikan bagi sekitar.",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-17T08:00:00+07:00",
  place: "Gedung Mutiara Ijen",
  address: "Jl. Ijen No. 25, Oro-oro Dowo, Klojen, Kota Malang",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2022", title: "Ta'aruf", body: "Dikenalkan oleh ustazah di kajian pekanan, kami bertukar biodata dengan niat yang sama: menyempurnakan separuh agama." },
    { date: "2026", title: "Khitbah", body: "Keluarga Hanif datang bersilaturahmi ke Malang dan melamar, disambut hangat oleh keluarga Alifa." },
    { date: "2027", title: "Akad", body: "Insyaallah kami menuju akad dengan restu kedua orang tua dan doa keluarga besar." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Jami' Malang", address: "Jl. Merdeka Barat No. 3, Kiduldalem, Klojen, Kota Malang" },
    { name: "Walimatul 'Ursy", date: "2027-04-17T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Gedung Mutiara Ijen", address: "Jl. Ijen No. 25, Oro-oro Dowo, Klojen, Kota Malang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7203 1704 27", account_name: "Alifa Nur Azizah" },
    { id: "demo-kado", type: "address", address: "Jl. Bunga Kemuning No. 14, Jatimulyo, Lowokwaru, Kota Malang 65141" },
  ],
  guestName: "Ibu Hj. Rahmawati & Keluarga",
  guestTable: "Meja Mint 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Pembukaan & tilawah", note: "Tamu putra dan putri di area terpisah" },
      { time: "11.20", title: "Tausiyah pernikahan" },
      { time: "11.50", title: "Ramah tamah & doa bersama" },
    ] },
    dressCode: { note: "Busana muslim yang sopan. Nuansa mint, putih, dan hijau lembut dipersilakan.", colors: ["#9ee0bd", "#ffffff", "#23875f", "#e6f5ee"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-04-17T08:00:00+07:00" },
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Imam Syafi'i", "Kel. Besar Drs. Abdul Hakim"] },
  },
});
