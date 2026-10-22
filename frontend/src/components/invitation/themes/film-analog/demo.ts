import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Bagas",
    brideFull: "Nadia Kirana Larasati",
    groomFull: "Bagas Pramudya Wicaksono",
    brideParents: "Putri dari\nBapak Teguh Santosa & Ibu Endang Rahayu",
    groomParents: "Putra dari\nBapak Hari Wicaksono & Ibu Retno Palupi",
    bridePhoto: "/themes/img/r27.webp",
    groomPhoto: "/themes/img/r26.webp",
    note: "Tiga puluh enam frame tidak pernah cukup. Kami ingin memotret sisa hidup bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T09:00:00+07:00",
  place: "Studio Kamar Gelap",
  address: "Jl. Sumur Bandung No. 12, Lebakgede, Coblong, Kota Bandung",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Juli 2020", title: "Roll pertama", body: "Kami bertemu di kelas cuci-cetak film. Nadia salah memasukkan film ke kamera Bagas, dan semua fotonya jadi double exposure." },
    { date: "2022", title: "Hunting tiap Minggu pagi", body: "Braga, Dago, kebun teh Pangalengan. Satu roll setiap minggu, ditukar dan dicetak bergantian." },
    { date: "Februari 2027", title: "Frame ke-36", body: "Di frame terakhir sebuah roll, Bagas memotret cincin di telapak tangannya. Nadia baru tahu saat fotonya selesai dicetak." },
  ],
  events: [
    { name: "Akad & Pemberkatan", date: "2027-10-09T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Studio Kamar Gelap", address: "Jl. Sumur Bandung No. 12, Lebakgede, Coblong, Kota Bandung" },
    { name: "Resepsi Kebun", date: "2027-10-09T15:30:00+07:00", time: "15.30 – 19.00 WIB", venue: "Halaman Belakang Studio Kamar Gelap", address: "Jl. Sumur Bandung No. 12, Lebakgede, Coblong, Kota Bandung" },
  ],
  gallery: [
    "/themes/img/a25.webp", "/themes/img/r42.webp", "/themes/img/r38.webp", "/themes/img/a123.webp",
    "/themes/img/a30.webp", "/themes/img/r75.webp", "/themes/img/a64.webp", "/themes/img/a122.webp",
  ],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 4477 05", account_name: "Nadia Kirana Larasati" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 2233 4455", account_name: "Bagas Pramudya" },
  ],
  guestName: "Mas Yoga & Partner",
  guestTable: "Frame 12",
  extras: {
    quote: { text: "Foto adalah cara kita berkata: aku pernah di sini, bersamamu, dan aku ingin mengingatnya.", source: "Catatan di balik foto pertama kami" },
    rundown: { items: [
      { time: "09.00", title: "Akad & pemberkatan", note: "Keluarga inti" },
      { time: "15.30", title: "Resepsi kebun dibuka" },
      { time: "16.30", title: "Sesi foto instan bersama tamu", note: "Kamera disediakan di setiap meja" },
      { time: "18.00", title: "Pemutaran slide kenangan" },
    ] },
    dressCode: { note: "Warna hangat ala foto lama: oranye bata, krem, hijau pudar, cokelat.", colors: ["#c8642a", "#efe4cc", "#5f7f6a", "#5a3a24"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut berbahagia", names: ["Keluarga Besar Santosa", "Keluarga Besar Wicaksono", "Klub Film Kamar Gelap"] },
    faq: { items: [
      { q: "Bolehkah membawa kamera?", a: "Sangat boleh! Kami akan senang menerima hasil cetak foto dari Anda." },
      { q: "Apakah acara di luar ruangan?", a: "Resepsi di kebun beratap tenda. Sore hari Bandung bisa dingin, bawalah jaket tipis." },
    ] },
  },
});
