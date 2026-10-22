import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Azizah", groom: "Hafiz",
    brideFull: "Nur Azizah Ramadhani, S.Pd.", groomFull: "Raja Muhammad Hafiz, S.T.",
    brideParents: "Putri bongsu dari\nBapak H. Syamsul Bahri & Ibu Hj. Zuraidah", groomParents: "Putra kedua dari\nBapak Raja Ahmad Yani & Ibu Hj. Fatimah Az-Zahra",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Lancang kuning berlayar malam, haluan menuju ke laut dalam. Kalau nakhoda kuranglah paham, alamat kapal akan tenggelam. Semoga kami menjadi nakhoda yang saling memahami.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-26T09:00:00+07:00",
  place: "Balai Adat Melayu Riau",
  address: "Jl. Diponegoro No. 39, Suka Mulia, Sail, Kota Pekanbaru, Riau",
  stories: [
    { date: "2020", title: "Bertemu di Siak", body: "Kami berkenalan saat festival tenun Siak. Hafiz menawar selendang, Azizah yang menenunnya." },
    { date: "2025", title: "Merisik & Meminang", body: "Keluarga Hafiz datang membawa tepak sirih dan pantun. Pinangan pun disambut dengan pantun pula." },
    { date: "2027", title: "Bersanding", body: "Dengan izin Allah, kami berlayar bersama dalam bahtera rumah tangga." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-26T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Raya An-Nur", address: "Jl. Hang Tuah No. 1, Sumahilang, Pekanbaru Kota, Riau" },
    { name: "Tepuk Tepung Tawar & Bersanding", date: "2027-06-26T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Adat Melayu Riau", address: "Jl. Diponegoro No. 39, Suka Mulia, Sail, Kota Pekanbaru, Riau" },
  ],
  gallery: ["/themes/img/r110.webp", "/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/r103.webp", "/themes/img/a21.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7311 2468 10", account_name: "Nur Azizah Ramadhani" },
    { id: "demo-brk", type: "bank", bank_name: "BRK Syariah", account_number: "811 22 33445", account_name: "Raja Muhammad Hafiz" },
  ],
  guestName: "Bapak H. Zainal Abidin & Keluarga",
  guestTable: "Meja Siak 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Berarak pengantin", note: "Diiringi kompang & silat persembahan" },
      { time: "11.30", title: "Tepuk tepung tawar" },
      { time: "12.00", title: "Bersanding di pelaminan" },
      { time: "12.30", title: "Makan berhidang", note: "Hidangan Melayu Riau" },
    ] },
    dressCode: { note: "Baju kurung atau teluk belanga. Kuning, hijau, dan biru laut dipersilakan.", colors: ["#e9b724", "#1f5b3a", "#1b5868", "#fbf1d4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-26T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syamsul Bahri", "Kel. Besar Raja Ahmad Yani"] },
  },
});
