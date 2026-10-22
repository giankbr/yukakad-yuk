import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gracia", groom: "Kevin",
    brideFull: "Gracia Natalia Lumentut, S.E.", groomFull: "Kevin Immanuel Rumengan, S.H., M.Kn.",
    brideParents: "Putri tunggal dari\nBapak Pdt. Hendrik Lumentut & Ibu Meiske Rorimpandey",
    groomParents: "Putra kedua dari\nBapak Johny Rumengan & Ibu Vonny Tumbelaka",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Kasih tidak pernah berkesudahan. Ia tumbuh pelan seperti bulu merak: helai demi helai, sampai suatu hari mekar sepenuhnya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T10:00:00+08:00",
  place: "Balai Merak, Kawasan Megamas",
  address: "Jl. Piere Tendean, Kawasan Megamas Blok C, Wenang, Kota Manado, Sulawesi Utara",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Desember 2020", title: "Paduan Suara Natal", body: "Gracia mengiringi piano, Kevin bernyanyi di barisan tenor. Latihan tiap Sabtu sore itu menjadi alasan kami saling menunggu minggu berikutnya." },
    { date: "2022 – 2026", title: "Jarak Jakarta–Manado", body: "Kevin menyelesaikan studi kenotariatan di Jakarta. Ribuan pesan, telepon tengah malam, dan doa yang sama setiap malam menjaga kami tetap dekat." },
    { date: "Maret 2027", title: "Lamaran", body: "Di hadapan kedua keluarga di Tomohon, Kevin meminta Gracia menjadi teman hidupnya. Jawabannya: ya, dengan berkat Tuhan." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-09-18T10:00:00+08:00", time: "10.00 – 12.00 WITA", venue: "GMIM Sentrum Manado", address: "Jl. Sam Ratulangi No. 1, Wenang Utara, Kota Manado, Sulawesi Utara" },
    { name: "Resepsi", date: "2027-09-18T18:00:00+08:00", time: "18.00 – 21.00 WITA", venue: "Balai Merak, Kawasan Megamas", address: "Jl. Piere Tendean, Kawasan Megamas Blok C, Wenang, Kota Manado, Sulawesi Utara" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/a31.webp", "/themes/img/a122.webp", "/themes/img/a33.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0152 0110 7766 503", account_name: "Gracia Natalia Lumentut" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0263 8841 70", account_name: "Kevin Immanuel Rumengan" },
  ],
  guestName: "Bapak Ronald Pangemanan & Keluarga",
  guestTable: "Meja Zamrud 4",
  extras: {
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "18.00", title: "Penyambutan tamu", note: "Musik kolintang & minuman selamat datang" },
      { time: "18.30", title: "Doa pembuka & sambutan keluarga" },
      { time: "19.00", title: "Makan malam", note: "Hidangan Minahasa & internasional" },
      { time: "20.00", title: "Dansa & foto bersama" },
    ] },
    dressCode: { note: "Formal malam dengan nuansa merak: toska, zamrud, biru tua, dan sentuhan emas.", colors: ["#0f3436", "#2f7d5b", "#1f8fa6", "#c9a24a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T10:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Lumentut – Rorimpandey", "Kel. Besar Rumengan – Tumbelaka"] },
    travel: { note: "Untuk tamu dari luar Manado, berikut beberapa pilihan menginap di sekitar Megamas.", items: [
      { name: "Hotel di kawasan Boulevard", detail: "± 500 m dari Balai Merak" },
      { name: "Antar-jemput bandara", detail: "Tersedia pada 17 September, mohon konfirmasi sebelumnya" },
    ] },
    faq: { items: [
      { q: "Apakah ibadah pemberkatan terbuka untuk umum?", a: "Ya, seluruh tamu dipersilakan mengikuti ibadah. Mohon hadir 15 menit sebelum dimulai." },
      { q: "Bolehkah membawa anak-anak?", a: "Tentu. Kami menyediakan area bermain kecil di sisi ballroom." },
    ] },
  },
});
