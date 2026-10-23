import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Rayyan",
    brideFull: "Nadhira Az-Zahra Salsabila", groomFull: "Rayyan Abdillah Fikri",
    brideParents: "Putri dari Bapak H. Ahmad Fauzan\n& Ibu Hj. Rahmi Kurniasih", groomParents: "Putra dari Bapak Drs. Syamsul Arifin\n& Ibu Nurul Hidayati",
    note: "Seperti tanah liat yang dibentuk perlahan lalu dibakar hingga kuat, semoga rumah tangga kami kokoh dan hangat dalam ridha-Nya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Kelas Keramik", body: "Kami bertemu di kelas membuat keramik akhir pekan. Mangkuk pertama kami sama-sama retak, dan dari situ obrolan dimulai." },
    { date: "2025", title: "Taaruf", body: "Dengan perantara guru mengaji Nadhira, kami berkenalan lebih sungguh-sungguh dan saling bertukar cita-cita." },
    { date: "Januari 2027", title: "Khitbah", body: "Keluarga Rayyan datang melamar dengan sederhana. Bismillah, kedua keluarga menyambut dengan hangat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Tanah Liat Dago", address: "Jl. Dago Giri No. 88, Mekarwangi, Kec. Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7212 0527 88", account_name: "Nadhira Az-Zahra Salsabila" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0220 5272 7", account_name: "Rayyan Abdillah Fikri" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Timur No. 14, Kec. Cibeunying Kaler, Kota Bandung 40191" },
  ],
  guestName: "Ibu Hj. Fatimah Zahra & Keluarga",
  guestTable: "Meja Lempung 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    dressCode: { note: "Busana muslim yang sopan. Nuansa tanah: terakota, krem, dan cokelat susu.", colors: ["#b5532e", "#f3e9dc", "#c8a36d", "#7a3218"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar H. Ahmad Fauzan", "Keluarga Besar Syamsul Arifin"] },
    faq: { items: [
      { q: "Apakah tamu pria dan wanita dipisah?", a: "Ya, area tamu pria dan wanita disediakan terpisah dengan pembatas." },
      { q: "Apakah tersedia tempat salat?", a: "Tersedia musala di Rumah Tanah Liat Dago." },
    ] },
  },
});
