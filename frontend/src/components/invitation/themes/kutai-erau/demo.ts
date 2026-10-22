import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Raudhah", groom: "Fikri",
    brideFull: "Siti Raudhatul Jannah, S.Pd.", groomFull: "Muhammad Fikri Ramadhan, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Syahrani Ismail & Ibu Hj. Masnah", groomParents: "Putra sulung dari\nBapak Ahmad Yani Kadir & Ibu Rusmiati",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Seperti Mahakam yang tak pernah berhenti mengalir, semoga kasih kami tenang, panjang, dan selalu memberi kehidupan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T09:00:00+08:00",
  place: "Masjid Jami' Aji Amir Hasanuddin",
  address: "Jl. Monumen Timur, Panji, Tenggarong, Kutai Kartanegara, Kalimantan Timur",
  stories: [
    { date: "2020", title: "Festival di Tepian Mahakam", body: "Kami berkenalan sebagai panitia lomba perahu saat pesta adat di Tenggarong. Raudhah memegang daftar peserta, Fikri yang selalu terlambat mendaftar." },
    { date: "2025", title: "Lamaran", body: "Keluarga Fikri datang membawa tanda ikatan. Dengan musyawarah dua keluarga, hari baik pun ditetapkan." },
    { date: "2027", title: "Akad Nikah", body: "Dengan memohon rida Allah, kami melangkah bersama di masjid tua Tenggarong, tak jauh dari sungai yang mempertemukan kami." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Jami' Aji Amir Hasanuddin", address: "Jl. Monumen Timur, Panji, Tenggarong, Kutai Kartanegara" },
    { name: "Walimatul 'Ursy", date: "2027-09-18T19:30:00+08:00", time: "19.30 – 22.00 WITA", venue: "Balai Pertemuan Umum Tenggarong", address: "Jl. Pahlawan, Timbau, Tenggarong, Kutai Kartanegara" },
  ],
  gallery: ["/themes/img/r1.webp", "/themes/img/r62.webp", "/themes/img/r64.webp", "/themes/img/r82.webp", "/themes/img/r77.webp"],
  gifts: [
    { id: "demo-bankaltimtara", type: "bank", bank_name: "Bankaltimtara Syariah", account_number: "0071 2045 5831", account_name: "Siti Raudhatul Jannah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7203 1188 46", account_name: "Muhammad Fikri Ramadhan" },
  ],
  guestName: "Bapak H. Abdul Rasyid & Keluarga",
  guestTable: "Meja Mahakam 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.30", title: "Penyambutan tamu", note: "Diiringi musik tingkilan Kutai" },
      { time: "20.00", title: "Doa & sambutan keluarga" },
      { time: "20.30", title: "Ramah tamah", note: "Nasi bekepor dan gangan asam" },
      { time: "21.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim resmi. Kuning, hijau, dan krem dipersilakan.", colors: ["#e8bf3e", "#2f5e3c", "#f7eecf", "#c99a2e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syahrani Ismail", "Kel. Besar Ahmad Yani Kadir"] },
  },
});
