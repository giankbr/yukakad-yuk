import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahma", groom: "Arsyad",
    brideFull: "Wa Ode Sitti Rahmawati, S.Pd.", groomFull: "La Ode Muhammad Arsyad, S.Kel.",
    brideParents: "Putri bungsu dari\nBapak La Ode Hamiru & Ibu Wa Ode Nursia", groomParents: "Putra kedua dari\nBapak H. La Ode Sabaruddin & Ibu Hj. Wa Ode Kamaria",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti kaghati kolope yang terbang tinggi karena benangnya dipegang erat, kami ingin saling menjaga sampai langit paling jauh.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-24T09:00:00+08:00",
  place: "Gedung Serbaguna Raha",
  address: "Jl. La Ode Pandu, Raha I, Kec. Katobu, Kabupaten Muna, Sulawesi Tenggara",
  stories: [
    { date: "2019", title: "Festival Layang-Layang", body: "Kami bertemu di festival kaghati di Raha. Arsyad membantu kakek Rahma menaikkan layang-layang daun kolope yang dirakitnya sendiri." },
    { date: "2022", title: "Gua Liang Kobori", body: "Dalam satu perjalanan keluarga, kami melihat lukisan layang-layang purba di dinding gua, dan bercerita tentang mimpi masing-masing." },
    { date: "2026", title: "Kafeompu", body: "Keluarga Arsyad datang melamar dengan adat Muna. Dengan restu kedua keluarga, hari baik pun disepakati." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-24T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Agung Raha", address: "Jl. Sultan Hasanuddin, Raha I, Kec. Katobu, Kabupaten Muna" },
    { name: "Resepsi", date: "2027-07-24T19:30:00+08:00", time: "19.30 – 22.00 WITA", venue: "Gedung Serbaguna Raha", address: "Jl. La Ode Pandu, Raha I, Kec. Katobu, Kabupaten Muna, Sulawesi Tenggara" },
  ],
  gallery: ["/themes/img/r103.webp", "/themes/img/r105.webp", "/themes/img/r38.webp", "/themes/img/r110.webp", "/themes/img/r104.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0412 0100 2231 509", account_name: "Wa Ode Sitti Rahmawati" },
    { id: "demo-kado", type: "address", address: "Jl. Gatot Subroto No. 21, Laende, Kec. Katobu, Raha, Kabupaten Muna 93611" },
  ],
  guestName: "Bapak La Ode Kaimuddin & Keluarga",
  guestTable: "Meja Kolope 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.30", title: "Kedatangan mempelai", note: "Diiringi rebana" },
      { time: "20.00", title: "Tari Linda", note: "Tarian adat Muna" },
      { time: "20.30", title: "Ramah tamah & jamuan" },
      { time: "21.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim atau tenun Muna. Merah, marun, kuning, dan hijau dipersilakan.", colors: ["#b3262a", "#6d1a2a", "#f0c23c", "#2f7a4f"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-24T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar La Ode Hamiru", "Kel. Besar H. La Ode Sabaruddin"] },
  },
});
