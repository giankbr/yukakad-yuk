import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aulia", groom: "Fikri",
    brideFull: "Aulia Rahmadani, S.Si.", groomFull: "Fikri Maulana Yusuf, S.T., M.T.",
    brideParents: "Putri kedua dari\nBapak H. Mochammad Ridwan & Ibu Hj. Siti Khotimah",
    groomParents: "Putra pertama dari\nBapak Dr. H. Yusuf Effendi & Ibu Hj. Lailatul Fitriyah",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Kami memilih memulai di waktu subuh: saat langit masih tenang, doa terasa dekat, dan hari baru menunggu untuk dijalani berdua.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-18T06:00:00+07:00",
  place: "Masjid Agung Jami' Kota Malang",
  address: "Jl. Merdeka Barat No. 3, Kiduldalem, Klojen, Kota Malang",
  stories: [
    { date: "2021", title: "Kajian Subuh", body: "Kami sering duduk di saf yang berjauhan pada kajian subuh kampus, hanya saling tahu nama dari daftar hadir." },
    { date: "2025", title: "Ta'aruf", body: "Seorang ustaz mempertemukan niat kami. Prosesnya sederhana, ditemani keluarga dan istikharah." },
    { date: "Mei 2027", title: "Khitbah", body: "Keluarga Fikri datang ke Malang; lamaran diterima pada pagi yang cerah selepas salat Duha." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T06:00:00+07:00", time: "06.00 – 07.30 WIB (ba'da Subuh)", venue: "Masjid Agung Jami' Kota Malang", address: "Jl. Merdeka Barat No. 3, Kiduldalem, Klojen, Kota Malang" },
    { name: "Walimatul 'Ursy", date: "2027-09-18T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Graha Cakrawala Universitas Negeri Malang", address: "Jl. Semarang No. 5, Sumbersari, Lowokwaru, Kota Malang" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/r15.webp", "/themes/img/r104.webp", "/themes/img/r10.webp", "/themes/img/r107.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7311 0825 46", account_name: "Aulia Rahmadani" },
    { id: "demo-bca", type: "bank", bank_name: "BCA Syariah", account_number: "0521 7788 90", account_name: "Fikri Maulana Yusuf" },
    { id: "demo-kado", type: "address", address: "Jl. Ijen Nirwana Blok B2 No. 14, Bareng, Klojen, Kota Malang 65116", account_name: "Keluarga H. Mochammad Ridwan" },
  ],
  guestName: "Bapak Ahmad Zainuddin & Keluarga",
  guestTable: "Meja Fajar 3",
  extras: {
    quote: { text: "Mahasuci Allah yang telah menciptakan semuanya berpasang-pasangan, baik dari apa yang ditumbuhkan oleh bumi dan dari diri mereka sendiri, maupun dari apa yang tidak mereka ketahui.", source: "QS. Yasin: 36" },
    rundown: { items: [
      { time: "06.00", title: "Akad nikah", note: "Selepas salat Subuh berjamaah" },
      { time: "07.00", title: "Sarapan bersama keluarga" },
      { time: "09.00", title: "Walimah dibuka" },
      { time: "11.30", title: "Doa penutup & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa fajar: biru muda, lilac, peach, atau krem.", colors: ["#b5c3e2", "#c9bfdc", "#f4c9b3", "#f3e6d4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T06:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Mochammad Ridwan", "Kel. Besar Dr. H. Yusuf Effendi"] },
  },
});
