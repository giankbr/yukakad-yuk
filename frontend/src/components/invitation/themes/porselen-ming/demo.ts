import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Livia", groom: "Adrian",
    brideFull: "Livia Hartanto, M.Sn.", groomFull: "Adrian Wijaya Kusuma, S.Ars.",
    brideParents: "Putri sulung dari\nBapak Hendra Hartanto & Ibu Melinda Susanto", groomParents: "Putra kedua dari\nBapak Budi Kusuma & Ibu Lanny Wijaya",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Seperti porselen yang dibakar dua kali, kami ingin cinta yang teruji api dan tetap jernih.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T16:00:00+07:00",
  place: "Balai Kartika Grand Ballroom",
  address: "Jl. Pemuda No. 150, Sekayu, Semarang Tengah, Kota Semarang",
  stories: [
    { date: "2019", title: "Ruang Restorasi", body: "Livia sedang merekatkan pecahan piring biru-putih di lokakarya museum, Adrian datang memotret koleksi untuk proyek arsitekturnya." },
    { date: "2022", title: "Pasar Antik", body: "Setiap Minggu pagi kami berburu keramik tua di Semarang. Yang kami bawa pulang kebanyakan cerita, bukan barang." },
    { date: "2027", title: "Sepasang Cawan", body: "Satu meja, dua cawan, dan keluarga yang merestui. Kami memulai koleksi kami sendiri." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-06-12T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Taman Kaca Balai Kartika", address: "Jl. Pemuda No. 150, Sekayu, Semarang Tengah, Kota Semarang" },
    { name: "Resepsi", date: "2027-06-12T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Balai Kartika Grand Ballroom", address: "Jl. Pemuda No. 150, Sekayu, Semarang Tengah, Kota Semarang" },
  ],
  gallery: ["/themes/img/a78.webp", "/themes/img/a77.webp", "/themes/img/a76.webp", "/themes/img/a74.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0095 1206 27", account_name: "Livia Hartanto" },
    { id: "demo-kado", type: "address", address: "Jl. Gajahmada No. 88, Kembangsari, Semarang Tengah, Kota Semarang 50133" },
  ],
  guestName: "Bapak Steven Halim & Keluarga",
  guestTable: "Meja Peoni 5",
  extras: {
    quote: { text: "Cinta itu sabar dan murah hati; ia tidak memegahkan diri, dan tidak sombong.", source: "Doa kami untuk rumah yang baru" },
    rundown: { items: [
      { time: "18.30", title: "Penerimaan tamu", note: "Teh melati & kudapan" },
      { time: "19.15", title: "Prosesi masuk & sambutan keluarga" },
      { time: "20.00", title: "Jamuan malam & foto bersama" },
    ] },
    dressCode: { note: "Formal. Biru kobalt, biru muda, dan putih gading dipersilakan.", colors: ["#1b3480", "#7d9bd6", "#f6f7f3", "#2f56a6"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-12T16:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak Hendra Hartanto", "Kel. Besar Bapak Budi Kusuma"] },
    faq: { items: [
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir basement Balai Kartika dan valet di lobi utama." },
      { q: "Boleh membawa anak?", a: "Tentu, kursi anak tersedia di area keluarga." },
    ] },
  },
});
