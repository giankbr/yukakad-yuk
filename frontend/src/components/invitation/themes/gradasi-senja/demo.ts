import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Maya", groom: "Dion",
    brideFull: "Maya Anindita Kusuma", groomFull: "Dionisius Arya Pratama",
    brideParents: "Putri dari\nBapak Hendro Kusuma & Ibu Lestari Wulandari", groomParents: "Putra dari\nBapak Yohanes Pratama & Ibu Maria Sri Rahayu",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Kami bertemu di sebuah pagi, dan memilih untuk menua bersama sampai senja.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T15:30:00+07:00",
  place: "Bukit Senja Venue",
  address: "Jl. Candi Ijo, Sambirejo, Prambanan, Kabupaten Sleman, DI Yogyakarta",
  stories: [
    { date: "Pagi · 2019", title: "Kereta pertama ke Yogyakarta", body: "Dua penumpang yang sama-sama ketiduran dan terlewat satu stasiun. Kami tertawa, lalu berbagi kopi sachet di peron." },
    { date: "Siang · 2023", title: "Rumah di dua kota", body: "Jakarta dan Yogyakarta, panggilan video setiap malam, dan akhir pekan yang selalu terasa terlalu cepat." },
    { date: "Senja · 2026", title: "Satu pertanyaan", body: "Di bukit yang sama tempat kami akan menikah, Dion bertanya, dan Maya menjawab sebelum matahari benar-benar turun." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-06-19T15:30:00+07:00", time: "15.30 – 16.30 WIB", venue: "Bukit Senja Venue", address: "Jl. Candi Ijo, Sambirejo, Prambanan, Kabupaten Sleman, DI Yogyakarta" },
    { name: "Resepsi Senja", date: "2027-06-19T17:00:00+07:00", time: "17.00 – 20.00 WIB", venue: "Teras Barat, Bukit Senja Venue", address: "Jl. Candi Ijo, Sambirejo, Prambanan, Kabupaten Sleman, DI Yogyakarta" },
  ],
  gallery: ["/themes/img/r109.webp", "/themes/img/r102.webp", "/themes/img/a33.webp", "/themes/img/r104.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0372 118 845", account_name: "Maya Anindita Kusuma" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 2671 0619", account_name: "Dionisius Arya Pratama" },
  ],
  guestName: "Mbak Nadine & Partner",
  guestTable: "Meja Jingga 4",
  extras: {
    rundown: { items: [
      { time: "15.30", title: "Upacara pernikahan", note: "Mohon hadir 15 menit lebih awal" },
      { time: "16.45", title: "Foto bersama di golden hour" },
      { time: "17.15", title: "Makan malam & pidato singkat" },
      { time: "18.30", title: "Dansa pertama setelah matahari terbenam" },
    ] },
    dressCode: { note: "Warna senja: peach, terakota lembut, lavender, atau ungu tua. Hindari putih.", colors: ["#f9c1a6", "#e98680", "#b86b8f", "#4e4282"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Acaranya di luar ruangan?", a: "Ya, upacara di halaman terbuka. Sepatu hak tipis kurang nyaman di rumput, jadi pilih alas kaki yang aman." },
      { q: "Bagaimana kalau hujan?", a: "Kami sudah menyiapkan tenda transparan di teras barat, jadi senjanya tetap terlihat." },
    ] },
  },
});
