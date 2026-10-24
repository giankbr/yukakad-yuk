import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Rendra",
    brideFull: "Ayu Kirana Putri", groomFull: "Rendra Aditya Pratama",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Tahun pertama itu seperti kertas: tipis, tapi bisa kami tulisi apa saja. Terima kasih sudah ikut membacanya.",
  },
  eventLabel: "Syukuran Satu Tahun Pernikahan",
  date: "2027-05-15T18:30:00+07:00",
  place: "Kediaman Ayu & Rendra",
  address: "Jl. Tebet Barat Dalam IV No. 12, Tebet, Jakarta Selatan",
  stories: [
    { date: "Mei 2026", title: "Hari Itu", body: "Kami menikah di Bogor. Hujan turun tepat saat sesi foto keluarga, dan ternyata itu foto yang paling kami suka." },
    { date: "Agustus 2026", title: "Kontrakan Pertama", body: "Pindah ke rumah kecil di Tebet. Lemari belum ada, tapi sudah ada dua cangkir yang serasi dan satu rak buku yang selalu penuh." },
    { date: "Desember 2026", title: "Belajar Masak", body: "Rendra akhirnya bisa membuat rendang tanpa gosong. Ayu tetap memegang rekor nasi goreng terbaik di rumah." },
    { date: "Mei 2027", title: "Surat Pertama", body: "Kado kertas untuk tahun pertama: kami saling menulis surat, dan ingin membacanya di depan orang-orang tersayang." },
  ],
  events: [
    { name: "Syukuran & Makan Malam", date: "2027-05-15T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Kediaman Ayu & Rendra", address: "Jl. Tebet Barat Dalam IV No. 12, Tebet, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/a131.webp", "/themes/img/r25.webp", "/themes/img/r7.webp", "/themes/img/a122.webp", "/themes/img/r8.webp"],
  gifts: [
    { id: "demo-donasi", type: "bank", bank_name: "BRI", account_number: "0341 0100 2277 509", account_name: "Taman Baca Kampung Tebet" },
  ],
  guestName: "Mbak Sinta & Mas Yoga",
  guestTable: "Meja Kertas 3",
  extras: {
    quote: { text: "Cinta yang paling awet bukan yang paling besar, tetapi yang setiap hari dipilih lagi.", source: "Surat Rendra untuk Ayu" },
    rundown: { items: [
      { time: "18.30", title: "Datang & ngobrol santai" },
      { time: "19.00", title: "Doa syukur", note: "Dipimpin Pak RT, Bapak H. Sobari" },
      { time: "19.20", title: "Membaca surat setahun", note: "Ayu dan Rendra saling membacakan surat" },
      { time: "19.45", title: "Makan malam bersama" },
    ] },
    dressCode: { note: "Santai rapi. Kalau sempat, pakai warna krem, koral, atau biru tinta.", colors: ["#f3e6d3", "#d66f60", "#2d3a5c", "#c39a6b"] },
    guestPass: {},
    rsvpDietary: {},
  },
});
