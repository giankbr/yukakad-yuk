import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Hendra",
    brideFull: "Sekar Melati Tanuwijaya, S.Ds.", groomFull: "Hendra Wirasantosa, S.T.",
    brideParents: "Putri pertama dari\nBapak Budi Tanuwijaya & Ibu Lestari Handayani", groomParents: "Putra kedua dari\nBapak Gunawan Wirasantosa & Ibu Lie Siok Hwa",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti kain tiga negeri yang dicelup berulang kali, kami belajar bahwa warna terindah lahir dari kesabaran.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T10:00:00+07:00",
  place: "Rumah Lawang Ombo",
  address: "Jl. Dasun, Desa Soditan, Kec. Lasem, Kab. Rembang, Jawa Tengah",
  stories: [
    { date: "2019", title: "Bertemu di Rumah Batik", body: "Sekar sedang belajar mencanting di sebuah rumah batik di Karangturi, Hendra datang memotret gang-gang Pecinan untuk tugas akhirnya." },
    { date: "2023", title: "Tiga Warna, Satu Kain", body: "Kami menunggui selembar kain tiga negeri dari celupan merah sampai sogan, dan sadar kami ingin menua bersama dengan sabar yang sama." },
    { date: "2027", title: "Pulang ke Lasem", body: "Dengan restu dua keluarga, kami kembali ke kota kecil di pesisir ini untuk mengikat janji." },
  ],
  events: [
    { name: "Upacara Pernikahan & Teh Pai", date: "2027-09-18T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "Rumah Lawang Ombo", address: "Jl. Dasun, Desa Soditan, Kec. Lasem, Kab. Rembang" },
    { name: "Resepsi", date: "2027-09-18T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Rumah Merah Heritage", address: "Jl. Karangturi Gg. IV No. 7, Desa Karangturi, Kec. Lasem, Kab. Rembang" },
  ],
  gallery: ["/themes/img/a31.webp", "/themes/img/a43.webp", "/themes/img/a26.webp", "/themes/img/a49.webp", "/themes/img/a25.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0331 2207 18", account_name: "Sekar Melati Tanuwijaya" },
    { id: "demo-kado", type: "address", address: "Jl. Untung Suropati No. 12, Desa Karangturi, Kec. Lasem, Kab. Rembang 59271" },
  ],
  guestName: "Bapak Santoso Handoko & Keluarga",
  guestTable: "Seruni 2",
  extras: {
    quote: { text: "Dua hati yang seia sekata, tajamnya mampu memotong logam; tutur katanya harum bagai anggrek.", source: "Kitab I Ching" },
    rundown: { items: [
      { time: "10.00", title: "Penyambutan keluarga", note: "Di pelataran Lawang Ombo" },
      { time: "10.30", title: "Upacara pernikahan" },
      { time: "11.15", title: "Teh Pai", note: "Penghormatan kepada orang tua dan para sesepuh" },
      { time: "18.30", title: "Resepsi & jamuan malam" },
    ] },
    dressCode: { note: "Batik pesisir atau kebaya encim. Merah, biru indigo, dan cokelat sogan dipersilakan.", colors: ["#a3242a", "#22355f", "#8a5527", "#efe3c8"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Budi Tanuwijaya", "Kel. Besar Bpk. Gunawan Wirasantosa", "Keluarga besar Tan & Lie, Lasem"] },
  },
});
