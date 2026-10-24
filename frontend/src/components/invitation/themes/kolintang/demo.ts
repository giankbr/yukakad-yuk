import { makeDemo } from "../demo-base";

// Pernikahan Kristen Minahasa di Tomohon: dua pemain kolintang jemaat yang bertemu di latihan ansambel gereja.
export const demo = makeDemo({
  couple: {
    bride: "Mikha", groom: "Rey",
    brideFull: "Mikhaela Grace Sondakh, S.Sn.", groomFull: "Raynaldo Lumingkewas, S.T.",
    brideParents: "Putri kedua dari\nBapak Johny Sondakh & Ibu Femmy Kawengian", groomParents: "Putra sulung dari\nBapak Ferry Lumingkewas & Ibu Deetje Tumbelaka",
    bridePhoto: "/themes/img/a127.webp", groomPhoto: "/themes/img/a126.webp",
    note: "Ia memegang melodi, saya menjaga bas. Sejak latihan kolintang pertama itu kami belajar bahwa lagu paling indah lahir dari dua nada yang saling mendengarkan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T10:00:00+08:00",
  place: "GMIM Sion Tomohon",
  address: "Jl. Raya Tomohon, Kel. Talete Satu, Kec. Tomohon Tengah, Kota Tomohon, Sulawesi Utara",
  stories: [
    { date: "Desember 2020", title: "Latihan Kolintang Natal", body: "Mikha baru pulang kuliah musik dan diminta melatih ansambel kolintang jemaat. Rey, yang biasanya cuma mengangkat peti alat, tiba-tiba ditunjuk memegang bas." },
    { date: "2023", title: "Festival Bunga Tomohon", body: "Kami tampil bersama di panggung festival, di antara kendaraan hias penuh krisan. Setelah lagu terakhir, Rey memberanikan diri mengajak makan malam di Kakaskasen." },
    { date: "Mei 2027", title: "Lamaran di Rumah Panggung", body: "Keluarga Lumingkewas datang ke rumah panggung keluarga Sondakh. Para tua-tua berembuk, doa dinaikkan, dan hari pemberkatan pun ditetapkan." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-09-18T10:00:00+08:00", time: "10.00 – 12.00 WITA", venue: "GMIM Sion Tomohon", address: "Jl. Raya Tomohon, Kel. Talete Satu, Kec. Tomohon Tengah, Kota Tomohon, Sulawesi Utara" },
    { name: "Resepsi & Malam Kolintang", date: "2027-09-18T18:00:00+08:00", time: "18.00 – 21.30 WITA", venue: "Wale Krisan Kakaskasen", address: "Jl. Raya Kakaskasen Dua, Kec. Tomohon Utara, Kota Tomohon (sebelah kebun bunga)" },
  ],
  gallery: ["/themes/img/r108.webp", "/themes/img/r8.webp", "/themes/img/r102.webp", "/themes/img/a133.webp", "/themes/img/r1.webp"],
  gifts: [
    { id: "demo-bsg", type: "bank", bank_name: "Bank SulutGo", account_number: "001 21 18 0457 21", account_name: "Mikhaela Grace Sondakh" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0412 0100 6638 504", account_name: "Raynaldo Lumingkewas" },
    { id: "demo-kado", type: "address", address: "Jl. Kakaskasen Dua, Lingkungan IV, Kec. Tomohon Utara, Kota Tomohon 95362", account_name: "Keluarga Sondakh" },
  ],
  guestName: "Bapak Hendrik Rondonuwu & Keluarga",
  guestTable: "Meja Krisan 3",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati; ia tidak cemburu. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu.", source: "1 Korintus 13:4, 7" },
    rundown: { items: [
      { time: "18.00", title: "Penyambutan tamu", note: "Diiringi ansambel kolintang jemaat GMIM Sion" },
      { time: "18.45", title: "Masuknya kedua mempelai & doa makan", note: "Dipimpin Pnt. Johanis Wenas" },
      { time: "19.15", title: "Santap malam", note: "Tinutuan, cakalang fufu, dan kue-kue Minahasa" },
      { time: "20.15", title: "Kolintang bersama & dansa Katrili" },
    ] },
    dressCode: { note: "Busana pesta rapi bernuansa Tomohon: hijau perbukitan, kuning krisan, merah muda, dan cokelat kayu.", colors: ["#2f5a3c", "#eba23a", "#e5636f", "#b9783a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Sondakh – Kawengian", "Kel. Besar Lumingkewas – Tumbelaka", "Ansambel Kolintang Jemaat GMIM Sion"] },
  },
});
