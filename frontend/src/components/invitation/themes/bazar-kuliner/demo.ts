import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Karang Taruna Kemuning", groom: "PKK RW 05",
    brideFull: "Karang Taruna Tunas Kemuning", groomFull: "Tim Penggerak PKK RW 05 Kemuning",
    brideParents: "Ketua panitia: Fajar Ramadhan\nKoordinator acara & panggung", groomParents: "Ketua: Ibu Ratih Wulandari\nKoordinator tenant & kebersihan",
    note: "Dua malam, empat puluh lapak, satu lapangan. Mari jajan bersama tetangga sambil mendukung usaha kecil di kampung kita.",
  },
  eventLabel: "Festival Jajan Kemuning",
  date: "2027-08-21T16:00:00+07:00",
  place: "Lapangan Serbaguna RW 05",
  address: "Jl. Kemuning Raya No. 5, Pejaten Timur, Pasar Minggu, Jakarta Selatan",
  story: { title: "Daftar Lapak", body: "" },
  stories: [
    { date: "Lapak 01 – 08", title: "Lorong Bakar-bakaran", body: "Sate Madura Cak Mamat, sate taichan Bang Udin, jagung bakar Mpok Nani, sosis dan bakso bakar Dapur Rini." },
    { date: "Lapak 09 – 18", title: "Lorong Manis & Gurih", body: "Martabak Bangka Ko Ahan, terang bulan mini, kue cubit lumer, pisang goreng madu, cireng isi, dan seblak Teh Euis." },
    { date: "Lapak 19 – 28", title: "Lorong Segar", body: "Es cendol gula aren, es doger, es teler, wedang jahe, kopi tubruk keliling, dan jus buah segar." },
    { date: "Panggung", title: "Musik, Lomba & Undian", body: "Orkes keroncong remaja, lomba makan kerupuk anak, demo masak ibu-ibu PKK, dan undian berhadiah setiap pukul 20.00." },
  ],
  events: [
    { name: "Malam Pertama: Pasar Senja", date: "2027-08-21T16:00:00+07:00", time: "16.00 – 22.00 WIB", venue: "Lapangan Serbaguna RW 05", address: "Jl. Kemuning Raya No. 5, Pejaten Timur, Pasar Minggu, Jakarta Selatan" },
    { name: "Malam Kedua: Lomba & Undian", date: "2027-08-22T16:00:00+07:00", time: "16.00 – 22.30 WIB", venue: "Lapangan Serbaguna RW 05", address: "Jl. Kemuning Raya No. 5, Pejaten Timur, Pasar Minggu, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r63.webp", "/themes/img/r64.webp", "/themes/img/a100.webp"],
  gifts: [
    { id: "demo-tenant", type: "bank", bank_name: "BRI", account_number: "0386 0100 2108 507", account_name: "Kas Karang Taruna Kemuning" },
    { id: "demo-qr", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 8821 0827", account_name: "Bendahara Panitia, Sinta" },
  ],
  guestName: "Keluarga Bapak Haryanto (RT 03)",
  guestTable: "Tiket Keluarga",
  extras: {
    rundown: { items: [
      { time: "16.00", title: "Lapak dibuka, musik akustik pembuka" },
      { time: "17.30", title: "Demo masak sambal bersama PKK" },
      { time: "19.00", title: "Orkes keroncong remaja Kemuning" },
      { time: "20.00", title: "Undian berhadiah untuk pengunjung" },
      { time: "22.00", title: "Lapak tutup, kerja bakti bersih lapangan" },
    ] },
    dressCode: { note: "Santai dan nyaman. Bawa tas belanja sendiri dan botol minum, kita kurangi sampah plastik bersama.", colors: ["#d9463b", "#f0b13a", "#1f8a86", "#fdf3e0"] },
    faq: { items: [
      { q: "Apakah masuknya gratis?", a: "Gratis untuk umum. Tiket di undangan ini hanya untuk undian berhadiah, tunjukkan di meja panitia." },
      { q: "Di mana parkir kendaraan?", a: "Parkir motor di halaman SDN Kemuning 02, mobil di sepanjang Jl. Kemuning Dalam. Dipandu petugas keamanan RW." },
      { q: "Bagaimana cara daftar jadi tenant?", a: "Hubungi panitia sebelum 10 Agustus 2027. Sewa lapak Rp150.000 untuk dua malam, sudah termasuk listrik dan meja." },
    ] },
  },
});
