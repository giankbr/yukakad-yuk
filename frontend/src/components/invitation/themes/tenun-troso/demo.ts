import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ainun", groom: "Rizal",
    brideFull: "Ainun Nisa Rahmawati, S.Pd.", groomFull: "Muhammad Rizal Ardiansyah, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Sholeh & Ibu Hj. Siti Maryam", groomParents: "Putra pertama dari\nBapak Sutrisno & Ibu Nur Hidayah",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti benang pakan yang diikat dan dicelup berkali-kali, kami belajar sabar sampai coraknya jadi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Rumah Keluarga Mempelai Wanita",
  address: "Desa Troso RT 03/RW 05, Kec. Pecangaan, Kabupaten Jepara, Jawa Tengah",
  stories: [
    { date: "2021", title: "Pameran Tenun Troso", body: "Ainun menjaga stan kain milik bapaknya, Rizal datang mencari kain untuk ibunya dan pulang membawa nomor telepon." },
    { date: "2024", title: "Belajar Menenun", body: "Setiap Ahad Rizal ikut belajar di ATBM keluarga Ainun. Kainnya masih miring, tapi niatnya lurus." },
    { date: "2027", title: "Satu Lembar Kain", body: "Dengan restu kedua keluarga, kami menenun lembar baru bersama di Bumi Kartini." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Baitul Muttaqin Troso", address: "Jl. Raya Troso, Kec. Pecangaan, Kabupaten Jepara" },
    { name: "Walimatul 'Ursy", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Rumah Keluarga Mempelai Wanita", address: "Desa Troso RT 03/RW 05, Kec. Pecangaan, Kabupaten Jepara" },
    { name: "Ngunduh Mantu", date: "2027-08-21T10:00:00+07:00", time: "10.00 – 14.00 WIB", venue: "Gedung Serbaguna Tahunan", address: "Jl. Pemuda, Kec. Tahunan, Kabupaten Jepara" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a22.webp", "/themes/img/a64.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0121 0100 5678 509", account_name: "Ainun Nisa Rahmawati" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2291 88", account_name: "Muhammad Rizal Ardiansyah" },
    { id: "demo-kado", type: "address", address: "Desa Troso RT 03/RW 05, Kec. Pecangaan, Kabupaten Jepara 59462" },
  ],
  guestName: "Bapak H. Masrukhan & Keluarga",
  guestTable: "Meja Pakan 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab manten", note: "Diiringi rebana dari Pecangaan" },
      { time: "11.30", title: "Sungkeman & doa" },
      { time: "12.00", title: "Ramah tamah", note: "Hidangan khas Jepara: pindang serani & horok-horok" },
    ] },
    dressCode: { note: "Batik atau tenun ikat. Merah bata, kunyit, dan nila dipersilakan.", colors: ["#93291f", "#c98a2e", "#26375c", "#efe2c6"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Sholeh", "Kel. Besar Bapak Sutrisno", "Paguyuban Penenun Troso"] },
  },
});
