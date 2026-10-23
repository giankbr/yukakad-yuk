import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laila", groom: "Hamzah",
    brideFull: "Laila Safitri Latuconsina, S.Farm.", groomFull: "Hamzah Ali Rumra, S.T.",
    brideParents: "Putri bungsu dari\nBapak Abdul Rahim Latuconsina & Ibu Hj. Siti Aminah Wakano", groomParents: "Putra kedua dari\nBapak Ali Usman Rumra & Ibu Nurlela Ollong",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti pala yang menyimpan fuli di dalam buahnya, kami ingin saling menjaga yang paling berharga.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T09:00:00+09:00",
  place: "Masjid Jami' Banda Neira",
  address: "Kelurahan Nusantara, Banda Neira, Kabupaten Maluku Tengah, Maluku",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Lomba Kora-kora", body: "Hamzah mendayung untuk regu Dwiwarna, Laila mencatat waktu di dermaga. Regu Hamzah kalah tipis, tapi menang satu nomor telepon." },
    { date: "2024", title: "Panen Pala", body: "Kami membantu keluarga memetik pala di kebun Lonthor. Di bawah pohon kenari, Hamzah menyampaikan niat baiknya." },
    { date: "2027", title: "Akad Nikah", body: "Dengan rida Allah dan restu kedua keluarga, kami menyatukan langkah di pulau tempat kami dibesarkan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T09:00:00+09:00", time: "09.00 – 10.30 WIT", venue: "Masjid Jami' Banda Neira", address: "Kelurahan Nusantara, Banda Neira, Kabupaten Maluku Tengah, Maluku" },
    { name: "Walimatul 'Ursy", date: "2027-06-19T19:30:00+09:00", time: "19.30 – 22.00 WIT", venue: "Gedung Pertemuan Kecamatan Banda", address: "Jl. Pelabuhan, Kelurahan Dwiwarna, Banda Neira, Kabupaten Maluku Tengah" },
  ],
  gallery: ["/themes/img/r103.webp", "/themes/img/r109.webp", "/themes/img/r102.webp", "/themes/img/r107.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7219 4408 31", account_name: "Laila Safitri Latuconsina" },
    { id: "demo-maluku", type: "bank", bank_name: "Bank Maluku Malut", account_number: "1002 7731 0458", account_name: "Hamzah Ali Rumra" },
  ],
  guestName: "Bapak Hi. Ismail Lamandasa & Keluarga",
  guestTable: "Meja Pala 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.30", title: "Penyambutan tamu", note: "Diiringi tifa dan totobuang" },
      { time: "20.00", title: "Doa & sambutan keluarga" },
      { time: "20.30", title: "Ramah tamah", note: "Ikan kuah pala, kue lapis, dan manisan pala" },
      { time: "21.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim resmi. Biru laut, putih, dan merah fuli dipersilakan.", colors: ["#24557e", "#f6f2e8", "#c0392b", "#e3a74c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Latuconsina – Wakano", "Kel. Besar Rumra – Ollong"] },
    travel: { note: "Banda Neira dapat dicapai lewat laut dari Ambon.", items: [
      { name: "Kapal cepat dari Ambon", detail: "± 6 jam dari Pelabuhan Tulehu, jadwal menyesuaikan cuaca" },
      { name: "Kapal Pelni", detail: "± 10 jam dari Pelabuhan Ambon, tiba di Pelabuhan Banda Neira" },
    ] },
  },
});
