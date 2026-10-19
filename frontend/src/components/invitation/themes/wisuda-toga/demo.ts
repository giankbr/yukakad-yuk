import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "",
    note: "Empat tahun belajar, begadang, dan bertumbuh. Kini saatnya bersyukur bersama orang-orang yang selalu mendukung.",
    brideFull: "Nadia Paramitha, S.Kom.",
    brideParents: "Sarjana Teknik Informatika\nUniversitas Nusantara Yogyakarta",
    bridePhoto: "/themes/img/r91.webp",
  },
  eventLabel: "Syukuran Wisuda",
  date: "2027-08-28T11:30:00+07:00",
  place: "Pendopo Keluarga Wijaya",
  address: "Jl. Palagan Tentara Pelajar No. 88, Ngaglik, Sleman, Yogyakarta",
  story: { title: "Perjalanan studi", body: "" },
  stories: [
    { date: "2023", title: "Mahasiswa baru", body: "Datang dari Purwokerto dengan satu koper dan tekad besar. Ikut UKM fotografi di minggu pertama." },
    { date: "2025", title: "Magang & asisten lab", body: "Enam bulan magang sebagai pengembang aplikasi, sambil menjadi asisten praktikum Basis Data." },
    { date: "2026", title: "Skripsi", body: "Meneliti aplikasi pendeteksi penyakit daun padi untuk petani. Banyak revisi, banyak kopi." },
    { date: "2027", title: "Lulus cum laude", body: "IPK 3,86 dan predikat dengan pujian. Terima kasih untuk setiap doa yang mengiringi." },
  ],
  events: [
    { name: "Prosesi Wisuda", date: "2027-08-28T07:30:00+07:00", time: "07.30 – 10.30 WIB (keluarga inti)", venue: "Auditorium Utama Universitas Nusantara", address: "Jl. Kaliurang Km 5, Caturtunggal, Sleman" },
    { name: "Syukuran & Makan Siang", date: "2027-08-28T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "Pendopo Keluarga Wijaya", address: "Jl. Palagan Tentara Pelajar No. 88, Ngaglik, Sleman" },
  ],
  gallery: ["/themes/img/r91.webp", "/themes/img/r94.webp", "/themes/img/r28.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "137 00 1234567 8", account_name: "Nadia Paramitha" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2765 4410", account_name: "Nadia Paramitha" },
  ],
  guestName: "Ibu Dewi Lestari & Keluarga",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "11.30", title: "Penyambutan tamu" },
      { time: "12.00", title: "Sambutan orang tua & doa syukur" },
      { time: "12.20", title: "Potong tumpeng", note: "Oleh wisudawati" },
      { time: "12.40", title: "Makan siang & foto bersama" },
    ] },
    dressCode: { note: "Batik atau smart casual, nuansa navy dan emas.", colors: ["#13294b", "#c8a24a", "#f6f4ef"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-28T07:30:00+07:00", note: "Saksikan prosesi wisuda dari rumah." },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Kami yang berbahagia", names: ["Bapak Herman Wijaya & Ibu Ratna Sari", "Mas Dimas Wijaya & Mbak Ayu", "Eyang Soedarsono (Purwokerto)"] },
    faq: { items: [
      { q: "Apakah tamu bisa ikut prosesi wisuda?", a: "Prosesi di auditorium terbatas untuk keluarga inti. Tamu dipersilakan langsung ke acara syukuran." },
      { q: "Ada area parkir?", a: "Tersedia parkir di halaman pendopo dan lapangan sebelahnya." },
    ] },
  },
});
