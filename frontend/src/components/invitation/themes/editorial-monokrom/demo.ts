import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Saskia", groom: "Raka",
    note: "Dua orang biasa, satu cerita yang kami tulis bersama — halaman demi halaman.",
    brideFull: "Saskia Anindita Putri, M.Ds.", groomFull: "Raka Pradipta Hadiningrat, S.Ars.",
    brideParents: "Putri tunggal dari\nBapak Adrian Setiadi & Ibu Maya Kartika", groomParents: "Putra ketiga dari\nBapak Rudy Hadiningrat & Ibu Sinta Lestari",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T10:00:00+07:00",
  place: "Ruang Serambi, Kemang",
  address: "Jl. Kemang Raya No. 47, Bangka, Mampang Prapatan, Jakarta Selatan",
  stories: [
    { date: "2017", title: "Studio lantai tiga", body: "Satu studio, dua meja gambar bersebelahan, dan lampu yang selalu menyala sampai pagi menjelang tenggat." },
    { date: "2021", title: "Pameran pertama", body: "Raka mengurus instalasi, Saskia menulis kuratorialnya. Sejak itu kami tahu kami bekerja paling baik berdua." },
    { date: "2026", title: "Satu pertanyaan", body: "Di galeri yang sepi setelah pameran ditutup, Raka bertanya. Saskia menjawab tanpa ragu." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Hikmah Kemang", address: "Jl. Kemang Selatan No. 12, Jakarta Selatan" },
    { name: "Resepsi", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Ruang Serambi, Kemang", address: "Jl. Kemang Raya No. 47, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r88.webp", "/themes/img/a74.webp", "/themes/img/r56.webp", "/themes/img/a78.webp", "/themes/img/r55.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1270 0098 7765 4", account_name: "Saskia Anindita Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka XI No. 3, Mampang Prapatan, Jakarta Selatan 12730" },
  ],
  guestName: "Sdr. Bima Arditya",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "11.00", title: "Resepsi dibuka" },
      { time: "12.00", title: "Makan siang & musik akustik" },
      { time: "13.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Hitam, putih, atau abu-abu. Potongan sederhana, tanpa motif ramai.", colors: ["#111111", "#f5f5f2", "#8a8a8a", "#cfcfcf"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Setiadi", "Kel. Besar Hadiningrat", "Rekan Studio Serambi"] },
    faq: { items: [
      { q: "Apakah ada area parkir?", a: "Tersedia parkir valet di lobi Ruang Serambi." },
      { q: "Boleh membawa anak?", a: "Tentu. Mohon cantumkan jumlah tamu saat konfirmasi." },
    ] },
  },
});
