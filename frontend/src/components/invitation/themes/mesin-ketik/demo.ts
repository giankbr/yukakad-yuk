import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Lintang", groom: "Bayu",
    brideFull: "Lintang Maharani Pratiwi", groomFull: "Bayu Adinegoro Santoso",
    brideParents: "Putri tunggal dari\nBapak Hendro Pratikno & Ibu Wulan Sari",
    groomParents: "Putra kedua dari\nBapak Gunawan Santoso & Ibu Retno Widuri",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Surat ini kami ketik pelan-pelan, satu huruf demi satu huruf, supaya Anda tahu: hari itu tidak lengkap tanpa kehadiran Anda.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T10:00:00+07:00",
  place: "Hotel Tugu Malang",
  address: "Jl. Tugu No. 3, Kiduldalem, Kec. Klojen, Kota Malang, Jawa Timur",
  stories: [
    { date: "Maret 2020", title: "Surat Pertama", body: "Kami berkenalan lewat komunitas sahabat pena. Surat pertama Bayu diketik dengan mesin ketik peninggalan kakeknya, lengkap dengan salah ketik di baris kedua." },
    { date: "2020 – 2024", title: "Seratus Dua Belas Amplop", body: "Malang ke Yogyakarta, bolak-balik lewat pos. Kami menyimpan setiap amplop dalam kotak sepatu yang kini sudah tiga." },
    { date: "Desember 2026", title: "Satu Kalimat", body: "Di lembar terakhir, Bayu hanya mengetik satu kalimat. Lintang menjawabnya dengan pena merah: iya." },
  ],
  events: [
    { name: "Ikrar Pernikahan", date: "2027-06-12T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Hotel Tugu Malang", address: "Jl. Tugu No. 3, Kiduldalem, Kec. Klojen, Kota Malang" },
    { name: "Resepsi", date: "2027-06-12T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Hotel Tugu Malang, Ruang Sriwijaya", address: "Jl. Tugu No. 3, Kiduldalem, Kec. Klojen, Kota Malang" },
  ],
  gallery: ["/themes/img/r44.webp", "/themes/img/a139.webp", "/themes/img/r43.webp", "/themes/img/a77.webp", "/themes/img/a76.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "3150 7712 08", account_name: "Lintang Maharani Pratiwi" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 3301 2706", account_name: "Bayu Adinegoro Santoso" },
    { id: "demo-kado", type: "address", address: "Jl. Ijen No. 41, Oro-oro Dowo, Kec. Klojen, Kota Malang 65119" },
  ],
  guestName: "Ibu Dra. Sri Rahayu & Keluarga",
  guestTable: "Meja 7",
  extras: {
    rundown: { items: [
      { time: "18.30", title: "Penerimaan tamu & tukar surat", note: "Tamu dipersilakan menulis kartu pos untuk kami" },
      { time: "19.00", title: "Kedatangan pengantin" },
      { time: "19.30", title: "Makan malam & musik keroncong" },
      { time: "20.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana formal klasik. Krem, cokelat tembakau, hijau sage, atau hitam.", colors: ["#f7f1e3", "#6b4f36", "#86ab9a", "#1f1d20"] },
    rsvpDietary: {},
    family: { names: ["Kel. Bapak Hendro Pratikno", "Kel. Bapak Gunawan Santoso"] },
    faq: { items: [
      { q: "Apakah ada area parkir?", a: "Tersedia parkir di halaman hotel dan di sepanjang Jl. Tugu." },
      { q: "Bolehkah membawa anak?", a: "Tentu, kami menyiapkan sudut mewarnai kartu pos untuk anak-anak." },
    ] },
  },
});
