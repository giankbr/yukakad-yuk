import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aurelia", groom: "Kevin",
    brideFull: "Aurelia Pramesti Wibisono", groomFull: "Kevin Adrianus Halim",
    brideParents: "Putri pertama dari\nBapak Hendro Wibisono & Ibu Lanny Kartika",
    groomParents: "Putra kedua dari\nBapak Steven Halim & Ibu Maria Goretti Susanti",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Kami bertemu di jalur pendakian, berteduh di pondok kayu yang sama, dan sejak itu selalu memilih jalan yang menanjak berdua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T10:00:00+07:00",
  place: "Pondok Pinus Cikole",
  address: "Jl. Raya Tangkuban Parahu Km. 9, Cikole, Lembang, Kabupaten Bandung Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Jalur Pendakian", body: "Satu rombongan pendakian ke Papandayan. Aurelia kehabisan air minum, Kevin kebetulan membawa dua botol." },
    { date: "2023", title: "Pondok di Lembang", body: "Akhir pekan yang selalu berakhir di pondok kayu dengan cokelat panas dan peta jalur yang belum pernah kami coba." },
    { date: "Desember 2026", title: "Di Puncak", body: "Di bawah langit pagi yang bersih, Kevin bertanya. Aurelia menjawab sebelum pertanyaannya selesai." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-07-17T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Padang Rumput Pondok Pinus Cikole", address: "Jl. Raya Tangkuban Parahu Km. 9, Cikole, Lembang, Kabupaten Bandung Barat" },
    { name: "Resepsi Kebun", date: "2027-07-17T12:30:00+07:00", time: "12.30 – 15.30 WIB", venue: "Rumah Kayu Cikole", address: "Jl. Raya Tangkuban Parahu Km. 9, Cikole, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/r81.webp", "/themes/img/r104.webp", "/themes/img/r89.webp", "/themes/img/a124.webp", "/themes/img/r84.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 1188 25", account_name: "Aurelia Pramesti Wibisono" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1320 0219 6641 7", account_name: "Kevin Adrianus Halim" },
    { id: "demo-kado", type: "address", address: "Jl. Setiabudhi No. 214, Isola, Sukasari, Kota Bandung 40154", account_name: "Aurelia & Kevin" },
  ],
  guestName: "Bapak Yohanes Prasetyo & Keluarga",
  guestTable: "Meja Edelweiss 4",
  extras: {
    quote: { text: "Mencintai bukan berarti saling memandang, tetapi bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Di padang rumput, mohon datang 15 menit lebih awal" },
      { time: "11.30", title: "Foto bersama", note: "Latar pinus dan kebun bunga" },
      { time: "12.30", title: "Resepsi kebun", note: "Makan siang ala rumah kayu" },
      { time: "15.00", title: "Cokelat panas & pelepasan" },
    ] },
    dressCode: { note: "Udara Lembang sejuk: busana rapi bernuansa padang bunga, dengan jaket atau syal tipis.", colors: ["#fbf7ee", "#76a94a", "#d6362c", "#2f5fc4", "#8a5230"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendro Wibisono", "Kel. Besar Bpk. Steven Halim", "Sahabat Pendaki Bandung"] },
    travel: { note: "Lembang bisa padat di akhir pekan. Berikut pilihan menginap dan parkir terdekat.", items: [
      { name: "Penginapan di Cikole", detail: "± 1 km dari lokasi, banyak pilihan pondok kayu" },
      { name: "Parkir & shuttle", detail: "Parkir di area utama, shuttle ke padang rumput tiap 10 menit" },
    ] },
    faq: { items: [
      { q: "Apakah acaranya di luar ruangan?", a: "Upacara di padang rumput terbuka. Resepsi di rumah kayu beratap, jadi aman bila hujan." },
      { q: "Sepatu apa yang sebaiknya dipakai?", a: "Hindari hak tinggi yang runcing karena area rumput. Sepatu datar atau hak tebal paling nyaman." },
    ] },
  },
});
