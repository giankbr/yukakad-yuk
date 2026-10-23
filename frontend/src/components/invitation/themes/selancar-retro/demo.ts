import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadira", groom: "Raka",
    brideFull: "Nadira Ayu Lestari", groomFull: "Raka Mahendra Putra",
    brideParents: "Putri dari Bapak Made Suardana\n& Ibu Kadek Lestari", groomParents: "Putra dari Bapak Agus Mahendra\n& Ibu Yuliana Sari",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Kami bertemu menunggu ombak yang sama. Sekarang kami ingin mengarunginya berdua, satu papan, satu arah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T16:00:00+08:00",
  place: "Rumah Pantai Sarasvati",
  address: "Jl. Pantai Batu Bolong No. 41, Canggu, Kuta Utara, Badung, Bali",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Juli 2021", title: "Kelas Selancar Pagi", body: "Nadira jatuh dari papan untuk ketujuh kalinya. Raka, instruktur pengganti hari itu, tidak berhenti tertawa lalu mengajarinya berdiri." },
    { date: "2023", title: "Road Trip Pesisir", body: "Dengan van tua penuh papan, kami menyusuri pantai dari Bali sampai Sumbawa, mengejar ombak dan matahari terbenam." },
    { date: "Februari 2027", title: "Di Ujung Ombak", body: "Saat matahari tenggelam, Raka menulis pertanyaan di pasir. Ombak hampir menghapusnya, tapi Nadira sempat menjawab: iya." },
    { date: "September 2027", title: "Satu Papan, Satu Arah", body: "Kami merayakan hari bahagia di tepi pantai tempat semuanya dimulai, bersama keluarga dan sahabat." },
  ],
  events: [
    { name: "Ikrar Janji di Tepi Pantai", date: "2027-09-18T16:00:00+08:00", time: "16.00 – 17.00 WITA", venue: "Pasir Utara, Rumah Pantai Sarasvati", address: "Jl. Pantai Batu Bolong No. 41, Canggu, Kuta Utara, Badung, Bali" },
    { name: "Pesta Senja & Api Unggun", date: "2027-09-18T18:00:00+08:00", time: "18.00 – 22.00 WITA", venue: "Teras Ombak, Rumah Pantai Sarasvati", address: "Jl. Pantai Batu Bolong No. 41, Canggu, Kuta Utara, Badung, Bali" },
  ],
  gallery: ["/themes/img/r9.webp", "/themes/img/r103.webp", "/themes/img/r11.webp", "/themes/img/r15.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0812 4477 90", account_name: "Nadira Ayu Lestari" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 3890 5521", account_name: "Raka Mahendra Putra" },
  ],
  guestName: "Mbak Sinta & Partner",
  guestTable: "Meja Papan 5",
  extras: {
    rundown: { items: [
      { time: "15.30", title: "Kelapa muda dan musik akustik menyambut tamu" },
      { time: "16.00", title: "Ikrar janji menghadap laut" },
      { time: "17.45", title: "Menyaksikan matahari terbenam bersama" },
      { time: "18.30", title: "Makan malam bakar-bakaran & api unggun" },
    ] },
    dressCode: { note: "Santai pantai: kemeja motif, linen, sundress. Warna senja dipersilakan. Sandal lebih nyaman daripada sepatu di atas pasir.", colors: ["#1d6a70", "#f2b440", "#ee8a35", "#f6e8cc"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Made Suardana", "Keluarga Besar Agus Mahendra"] },
    faq: { items: [
      { q: "Apakah ada parkir?", a: "Parkir motor dan mobil tersedia di depan Rumah Pantai. Jalan menuju pantai sempit, kami sarankan berbagi kendaraan." },
      { q: "Bolehkah membawa papan selancar?", a: "Boleh! Ombak sore di Batu Bolong cukup ramah. Ada rak papan dan bilas air tawar di samping teras." },
    ] },
  },
});
