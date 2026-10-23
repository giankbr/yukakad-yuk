import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Hafiz",
    brideFull: "Salma Khairunnisa, S.Farm.", groomFull: "Muhammad Hafiz Al-Amin, Lc.",
    brideParents: "Putri ketiga dari\nBapak H. Abdul Karim & Ibu Hj. Rahmah", groomParents: "Putra sulung dari\nBapak KH. Zainal Abidin & Ibu Nyai Hj. Fauziah",
    note: "Di bawah langit yang sama, bintang-bintang mengajari kami arah pulang.",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-17T08:00:00+07:00",
  place: "Gedung Sasana Kencana",
  address: "Jl. Ahmad Yani No. 128, Gayungan, Surabaya",
  stories: [
    { date: "2020", title: "Kairo", body: "Hafiz menempuh studi di Al-Azhar, Salma datang untuk program musim panas farmasi. Kami berkenalan di sebuah kajian pelajar Indonesia." },
    { date: "2023", title: "Malam di Sinai", body: "Rombongan pelajar bermalam di kaki gunung. Di bawah langit penuh bintang, kami sama-sama berdoa untuk jalan yang lurus." },
    { date: "2027", title: "Mitsaqan Ghalizha", body: "Setelah istikharah dan restu kedua keluarga, kami mengikat janji yang kokoh di Surabaya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Nasional Al-Akbar", address: "Jl. Masjid Al-Akbar Timur No. 1, Gayungan, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-04-17T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Gedung Sasana Kencana", address: "Jl. Ahmad Yani No. 128, Gayungan, Surabaya" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/a33.webp", "/themes/img/a123.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 4455 19", account_name: "Salma Khairunnisa" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "141 00 2027 0417", account_name: "Muhammad Hafiz Al-Amin" },
  ],
  guestName: "Ustadz Ahmad Fauzan & Keluarga",
  guestTable: "Meja Bintang 3",
  extras: {
    quote: { text: "Maha Suci Allah yang menjadikan di langit gugusan bintang dan Dia menjadikan padanya matahari dan bulan yang bercahaya.", source: "QS. Al-Furqan: 61" },
    rundown: { items: [
      { time: "19.00", title: "Kedatangan tamu", note: "Hidangan pembuka & gambus" },
      { time: "19.30", title: "Tausiyah pernikahan" },
      { time: "20.15", title: "Doa bersama & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim formal. Nuansa malam: biru tua, ungu senja, dan krem pasir.", colors: ["#111940", "#4a4170", "#d9b46a", "#efe4d2"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-04-17T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Karim", "Kel. Besar KH. Zainal Abidin"] },
  },
});
