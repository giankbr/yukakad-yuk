import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Raka", groom: "Salsa",
    brideFull: "Raka Aditya Pramudya", groomFull: "Salsabila Nur Azizah",
    brideParents: "XII MIPA 2\nKetua Angkatan 2027", groomParents: "XII IPS 1\nKetua OSIS 2026/2027",
    bridePhoto: "/themes/img/r101.webp", groomPhoto: "/themes/img/r100.webp",
    note: "Tiga tahun berseragam putih abu-abu, satu malam untuk merayakannya. Datang dengan gaya terbaikmu, Angkatan 27!",
  },
  eventLabel: "Malam Perpisahan",
  date: "2027-06-12T18:30:00+07:00",
  place: "Ballroom Graha Candi Asri",
  address: "Jl. Pandanaran No. 88, Pekunden, Semarang Tengah, Kota Semarang",
  story: { title: "", body: "" },
  stories: [
    { date: "Juli 2024", title: "MPLS & seragam baru", body: "Datang dengan tas kebesaran dan nama di papan karton. Belum saling kenal, sudah disuruh bernyanyi mars sekolah." },
    { date: "2025", title: "Pensi & study tour", body: "Panggung pensi di lapangan basket, lalu bus rombongan ke Bali yang penuh nyanyian sampai subuh." },
    { date: "Mei 2027", title: "Lulus bersama", body: "Ujian selesai, pengumuman keluar, dan semua lulus. Saatnya berpamitan dengan cara paling meriah." },
  ],
  events: [
    { name: "Pelepasan Siswa Kelas XII", date: "2027-06-12T15:00:00+07:00", time: "15.00 – 17.00 WIB", venue: "Aula SMA Harapan Nusantara", address: "Jl. Menteri Supeno No. 1, Mugassari, Semarang Selatan, Kota Semarang" },
    { name: "Gala Dinner & Prom Night", date: "2027-06-12T18:30:00+07:00", time: "18.30 – 22.00 WIB", venue: "Ballroom Graha Candi Asri", address: "Jl. Pandanaran No. 88, Pekunden, Semarang Tengah, Kota Semarang" },
  ],
  gallery: ["/themes/img/r78.webp", "/themes/img/r77.webp", "/themes/img/a140.webp", "/themes/img/r79.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0091 0100 7720 503", account_name: "Nabila Putri (Bendahara Angkatan)" },
  ],
  guestName: "Dimas Prakoso",
  guestTable: "XII MIPA 2",
  extras: {
    rundown: { items: [
      { time: "18.30", title: "Red carpet & photobooth", note: "Foto per kelas di backdrop bintang" },
      { time: "19.15", title: "Gala dinner & sambutan wali kelas" },
      { time: "20.00", title: "Penganugerahan Prom King & Queen", note: "Plus kategori paling kocak sekelas" },
      { time: "20.45", title: "Band angkatan & dansa terakhir" },
    ] },
    dressCode: { note: "Tema Midnight Glam: gaun, kebaya modern, batik, atau jas. Warna malam dengan sentuhan kilau.", colors: ["#1b1a4a", "#d9dbe6", "#e8459a", "#0b0720"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Panitia Perpisahan", names: ["Raka & Salsa (Ketua)", "Nabila Putri (Bendahara)", "Bagas & Clarissa (Acara)", "Tim Dokumentasi XII IPS 3"] },
    faq: { items: [
      { q: "Siapa saja yang diundang?", a: "Seluruh siswa kelas XII, wali kelas, guru, dan orang tua yang ingin hadir saat pelepasan sore." },
      { q: "Jam berapa acara selesai?", a: "Pukul 22.00 WIB. Orang tua bisa menjemput di lobi barat Graha Candi Asri." },
      { q: "Apakah ada iuran?", a: "Iuran sudah lewat kas kelas. Sumbangan sukarela untuk kenang-kenangan sekolah tertera di bawah." },
    ] },
  },
});
