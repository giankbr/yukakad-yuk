import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Farhan",
    brideFull: "Fatimah Az-Zahra Rahmani, S.Ars.", groomFull: "Muhammad Farhan Alatas, S.T.",
    brideParents: "Putri pertama dari\nBapak H. Syamsul Rahman & Ibu Hj. Nadia Fauziah", groomParents: "Putra ketiga dari\nBapak H. Umar Alatas & Ibu Hj. Salma Baraqbah",
    note: "Satu bata tak berarti apa-apa sampai ia disusun bersama yang lain. Kami ingin menyusun rumah itu, pelan-pelan, bata demi bata.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-11-13T08:00:00+07:00",
  place: "Masjid Raya Al-Falah",
  address: "Jl. Raya Darmo No. 137A, Wonokromo, Surabaya",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Studio yang sama", body: "Kami satu kelompok di studio arsitektur. Zahra menggambar denah, Farhan sibuk menghitung jumlah bata." },
    { date: "2024", title: "Isfahan", body: "Dalam perjalanan riset ke Isfahan kami menghabiskan sore memotret dinding bata bermotif. Di sana Farhan memberanikan diri bicara soal masa depan." },
    { date: "2027", title: "Akad Nikah", body: "Dengan memohon rida Allah, kami mengikat janji suci di hadapan keluarga dan sahabat di Surabaya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-11-13T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Raya Al-Falah", address: "Jl. Raya Darmo No. 137A, Wonokromo, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-11-13T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Hotel Majapahit Surabaya", address: "Jl. Tunjungan No. 65, Genteng, Surabaya" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a18.webp", "/themes/img/a125.webp", "/themes/img/a118.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 4458 30", account_name: "Fatimah Az-Zahra Rahmani" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "142 00 1987 655 2", account_name: "Muhammad Farhan Alatas" },
  ],
  guestName: "Bapak Dr. H. Hasan Assegaf & Keluarga",
  guestTable: "Meja Firuzeh 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu", note: "Diiringi gambus dan hadrah" },
      { time: "11.30", title: "Kirab pengantin" },
      { time: "12.00", title: "Doa & sambutan keluarga" },
      { time: "12.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim resmi. Nuansa pirus, biru kobalt, dan krem bata dipersilakan.", colors: ["#2a9893", "#22488a", "#f3e8d6", "#c9a06a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syamsul Rahman", "Kel. Besar H. Umar Alatas"] },
    faq: { items: [
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir di basement hotel dan gedung parkir Tunjungan." },
      { q: "Di mana tempat salat?", a: "Musala tersedia di lantai dasar, dekat ballroom." },
    ] },
  },
});
