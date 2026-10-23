import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    brideFull: "Arkana Bagas Wicaksono",
    brideParents: "Putra kedua dari Bapak Dimas Wicaksono & Ibu Laras Pramesti",
    note: "Abrakadabra! Arka genap enam tahun dan ingin mengundang teman-teman menonton pertunjukan sulap paling seru, lengkap dengan kelinci, kartu ajaib, dan kue ulang tahun.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-10-09T15:30:00+07:00",
  place: "Aula Serbaguna Cluster Bougenville",
  address: "Jl. Bougenville Raya No. 2, Kota Wisata, Gunung Putri, Kabupaten Bogor",
  story: { title: "Cerita Arka", body: "" },
  stories: [
    { date: "2021", title: "Si kecil datang", body: "Arka lahir di pagi yang cerah bulan Oktober, langsung jadi pusat perhatian seisi rumah." },
    { date: "2024", title: "Trik pertama", body: "Arka menyembunyikan koin di balik telinga Kakek dan tertawa paling keras ketika Kakek pura-pura kaget." },
    { date: "2026", title: "Masuk TK", body: "Di hari pentas seni, Arka tampil dengan topi tinggi dari karton dan tongkat dari sedotan." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang Arka hafal tiga trik kartu, suka kelinci, dan bercita-cita jadi pesulap terkenal." },
  ],
  events: [
    { name: "Pertunjukan Ulang Tahun Arka", date: "2027-10-09T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Aula Serbaguna Cluster Bougenville", address: "Jl. Bougenville Raya No. 2, Kota Wisata, Gunung Putri, Kabupaten Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "8730 552 190", account_name: "Laras Pramesti" },
    { id: "demo-kado", type: "address", address: "Cluster Bougenville Blok C7 No. 15, Kota Wisata, Gunung Putri, Kabupaten Bogor 16968" },
  ],
  guestName: "Adik Kayla & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arkana Bagas Wicaksono", nickname: "Arka", birthDate: "2021-10-09T07:10:00+07:00", parents: "Putra kedua dari Bapak Dimas Wicaksono & Ibu Laras Pramesti" },
    rundown: { items: [
      { time: "15.30", title: "Pintu panggung dibuka", note: "Setiap tamu kecil dapat topi pesulap dan tongkat ajaib" },
      { time: "16.00", title: "Pertunjukan sulap", note: "Kak Rendy dan kelinci putihnya, Mochi" },
      { time: "16.45", title: "Lomba tebak kartu & sulap bersama" },
      { time: "17.15", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Datang sebagai pesulap kecil! Jubah, topi, dasi kupu-kupu, atau baju ungu dan hitam favoritmu.", colors: ["#1d1a45", "#7a2e98", "#eab54a", "#c8324a"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Wicaksono", "Eyang Putri Pramesti", "Kak Nara (kakak Arka)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi kejutan terbaik. Kalau ingin memberi, ini yang sedang Arka impikan.", items: [
      { id: "w1", name: "Set sulap anak 100 trik", price: "± Rp150.000" },
      { id: "w2", name: "Buku cerita pesulap cilik", price: "± Rp75.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Jubah & topi pesulap", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh ikut menonton?", a: "Tentu! Kursi Ayah dan Bunda disiapkan di belakang barisan anak-anak." },
      { q: "Apakah ada kelinci sungguhan?", a: "Ada, Mochi si kelinci pesulap. Anak-anak boleh mengelusnya bersama pendamping setelah pertunjukan." },
    ] },
  },
});
