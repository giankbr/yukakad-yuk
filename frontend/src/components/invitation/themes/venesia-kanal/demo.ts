import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Livia", groom: "Adrian",
    brideFull: "Livia Anastasia Wirawan, M.Ars.", groomFull: "Adrian Satria Nugroho, S.E.",
    brideParents: "Putri sulung dari\nBapak Hendra Wirawan & Ibu Melinda Santoso", groomParents: "Putra kedua dari\nBapak Bambang Nugroho & Ibu Ratna Kusumawati",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Kami pernah tersesat di gang-gang Venesia dan menemukan bahwa jalan pulang terbaik adalah berjalan bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T16:00:00+07:00",
  place: "Taman Gedung Arsip Nasional",
  address: "Jl. Gajah Mada No. 111, Krukut, Kec. Taman Sari, Jakarta Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Studio Arsitektur", body: "Livia sedang menggambar sketsa jembatan untuk tugas akhir. Adrian, teman kakaknya, tidak sengaja menumpahkan kopi di atasnya dan berjanji menggantinya dengan makan malam." },
    { date: "2023", title: "Tersesat di Venesia", body: "Liburan pertama kami ke Italia. Tanpa peta, kami menyusuri kanal kecil sampai senja dan menemukan jembatan batu yang mirip sketsa Livia dulu." },
    { date: "2026", title: "Di Atas Jembatan", body: "Kembali ke kota yang sama, Adrian berlutut di jembatan itu. Gondola lewat di bawah dan pendayungnya ikut bertepuk tangan." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-09-18T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Taman Gedung Arsip Nasional", address: "Jl. Gajah Mada No. 111, Krukut, Kec. Taman Sari, Jakarta Barat" },
    { name: "Resepsi Pernikahan", date: "2027-09-18T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Aula Kanal, Gedung Arsip Nasional", address: "Jl. Gajah Mada No. 111, Krukut, Kec. Taman Sari, Jakarta Barat" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/r56.webp", "/themes/img/a123.webp", "/themes/img/r85.webp", "/themes/img/r43.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5210 448 913", account_name: "Livia Anastasia Wirawan" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1240 0137 7726 4", account_name: "Adrian Satria Nugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Pluit Karang Indah Timur No. 28, Pluit, Kec. Penjaringan, Jakarta Utara 14450" },
  ],
  guestName: "Ibu Margaretha Lim & Keluarga",
  guestTable: "Meja Rialto 5",
  extras: {
    quote: { text: "Cinta tidak saling memandang, tetapi bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "18.30", title: "Aperitivo & musik akustik", note: "Lagu-lagu Italia lama oleh kuartet gesek" },
      { time: "19.00", title: "Masuknya kedua mempelai" },
      { time: "19.30", title: "Makan malam bersama", note: "Menu pasta, risotto, dan tiramisu" },
      { time: "20.45", title: "Dansa pertama & potong kue" },
    ] },
    dressCode: { note: "Semi formal bernuansa pastel: merah muda, kuning gading, peach, dan hijau kanal.", colors: ["#e7a99a", "#efc57e", "#5f9a94", "#22344d"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Wirawan – Santoso", "Kel. Besar Nugroho – Kusumawati"] },
    faq: { items: [
      { q: "Apakah upacara di luar ruangan?", a: "Ya, di taman. Jika hujan, upacara dipindahkan ke aula yang sama dengan resepsi." },
      { q: "Di mana tempat parkir?", a: "Parkir tersedia di halaman Gedung Arsip dan gedung parkir Jl. Gajah Mada, valet disediakan." },
    ] },
  },
});
