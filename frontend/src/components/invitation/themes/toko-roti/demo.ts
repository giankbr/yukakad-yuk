import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anya", groom: "Gilang",
    brideFull: "Anya Kirana Hadiwijaya", groomFull: "Gilang Pradipta Nugraha",
    brideParents: "Putri bungsu dari\nBapak Hendra Hadiwijaya & Ibu Lily Susanto", groomParents: "Putra pertama dari\nBapak Agus Nugraha & Ibu Wulan Sari",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Resep kami sederhana: sejumput sabar, segenggam tawa, dan diuleni setiap hari dengan sayang. Kami tunggu di meja paling hangat.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T10:00:00+07:00",
  place: "Hotel Savoy Homann",
  address: "Jl. Asia Afrika No. 112, Cikawao, Kec. Lengkong, Kota Bandung",
  stories: [
    { date: "2022", title: "Roti tawar jam enam pagi", body: "Gilang selalu datang paling pagi ke toko roti keluarga Anya di Braga. Selalu roti tawar gandum, selalu minta diiris tipis." },
    { date: "2024", title: "Kue yang gosong", body: "Anya mencoba resep bolu baru dan gagal total. Gilang tetap menghabiskannya, lalu menawarkan diri jadi pencicip tetap." },
    { date: "2026", title: "Cincin di dalam kotak kue", body: "Di sebuah kotak berpita merah-putih, di sebelah croissant kesukaan Anya, ada cincin kecil dan secarik kartu: maukah kamu?" },
  ],
  events: [
    { name: "Pemberkatan & Akad", date: "2027-10-16T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Hotel Savoy Homann, Ruang Panghegar", address: "Jl. Asia Afrika No. 112, Cikawao, Kec. Lengkong, Kota Bandung" },
    { name: "Resepsi & Pesta Kue", date: "2027-10-16T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Toko Roti Sinar Pagi (halaman belakang)", address: "Jl. Braga No. 47, Braga, Kec. Sumur Bandung, Kota Bandung" },
  ],
  gallery: ["/themes/img/a23.webp", "/themes/img/r92.webp", "/themes/img/r28.webp", "/themes/img/r26.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 2281 96", account_name: "Anya Kirana Hadiwijaya" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0255 7719 8", account_name: "Gilang Pradipta Nugraha" },
    { id: "demo-kado", type: "address", address: "Toko Roti Sinar Pagi, Jl. Braga No. 47, Kota Bandung 40111" },
  ],
  guestName: "Kak Rara & Partner",
  guestTable: "Meja Croissant 4",
  extras: {
    rundown: { items: [
      { time: "18.30", title: "Sambutan & roti hangat", note: "Roti sobek dan teh melati untuk tamu yang datang" },
      { time: "19.15", title: "Potong kue pengantin", note: "Kue tiga tingkat buatan Ibu Lily" },
      { time: "19.45", title: "Makan malam bersama" },
      { time: "20.30", title: "Bawa pulang kotak kue", note: "Satu kotak untuk setiap undangan" },
    ] },
    dressCode: { note: "Santai rapi bernuansa toko roti: krem, merah ceri, hijau pistachio, dan cokelat.", colors: ["#fbf1e2", "#c63d4b", "#9cc5a1", "#5a3826"] },
    rsvpDietary: { label: "Ada alergi (gluten, telur, kacang)? (opsional)" },
    family: { names: ["Kel. Hendra Hadiwijaya", "Kel. Agus Nugraha"] },
    faq: { items: [
      { q: "Ada area parkir?", a: "Parkir tersedia di Hotel Savoy Homann. Ke Braga cukup berjalan kaki lima menit." },
      { q: "Boleh membawa anak?", a: "Tentu! Ada meja hias kue kecil untuk anak-anak saat resepsi." },
    ] },
  },
});
