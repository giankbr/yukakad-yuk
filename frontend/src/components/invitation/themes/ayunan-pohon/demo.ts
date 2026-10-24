import { makeDemo } from "../demo-base";

// Pernikahan bergaya buku cerita: pohon tua di bukit, ayunan tali, padang rumput saat senja. Lembang, musim kemarau.
export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Gilang",
    brideFull: "Kirana Ayu Pramesti", groomFull: "Gilang Mahardika Putra",
    brideParents: "Putri kedua dari\nBapak Hendra Pramono & Ibu Lestari Wulan", groomParents: "Putra sulung dari\nBapak Agus Mahendra & Ibu Rina Kartika",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Ada pohon tua di bukit belakang rumah nenek. Di ayunannya kami dulu bergantian mendorong, sekarang kami ingin berayun bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-28T15:30:00+07:00",
  place: "Padang Rumput Bukit Senja",
  address: "Jl. Kolonel Masturi Km. 9, Cikahuripan, Kec. Lembang, Kabupaten Bandung Barat",
  stories: [
    { date: "2016", title: "Tetangga Liburan", body: "Setiap libur kenaikan kelas kami bertemu di rumah nenek masing-masing, berebut giliran di ayunan pohon yang sama." },
    { date: "2022", title: "Bertemu Lagi", body: "Gilang pulang dari Surabaya, Kirana baru lulus. Ayunan itu masih ada, talinya saja yang sudah diganti." },
    { date: "2026", title: "Di Bawah Pohon", body: "Saat senja dan kunang-kunang mulai keluar, Gilang bertanya dengan suara gugup. Kirana menjawab sebelum pertanyaannya selesai." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-08-28T15:30:00+07:00", time: "15.30 – 16.30 WIB", venue: "Padang Rumput Bukit Senja", address: "Jl. Kolonel Masturi Km. 9, Cikahuripan, Kec. Lembang, Kabupaten Bandung Barat" },
    { name: "Resepsi Senja", date: "2027-08-28T17:00:00+07:00", time: "17.00 – 20.00 WIB", venue: "Rumah Kayu Bukit Senja", address: "Jl. Kolonel Masturi Km. 9, Cikahuripan, Kec. Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/a111.webp", "/themes/img/a116.webp", "/themes/img/a132.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 2211 86", account_name: "Kirana Ayu Pramesti" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2044 7319", account_name: "Gilang Mahardika Putra" },
    { id: "demo-kado", type: "address", address: "Jl. Cihanjuang Indah No. 7, Parongpong, Bandung Barat 40559" },
  ],
  guestName: "Mas Raka & Mbak Tia",
  guestTable: "Meja Kunang-kunang 2",
  extras: {
    quote: { text: "Cinta tidak saling menatap, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "15.30", title: "Janji di bawah pohon" },
      { time: "17.00", title: "Teh sore & piknik di padang", note: "Tikar dan selimut disediakan" },
      { time: "18.30", title: "Makan malam & lampu gantung", note: "Jaket hangat sangat dianjurkan" },
    ] },
    dressCode: { note: "Warna padang senja: krem, hijau zaitun, kuning madu, dan oranye bata. Sepatu datar lebih nyaman di rumput.", colors: ["#f3e3c2", "#6f7f45", "#e0b45a", "#c2643c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Bapak Hendra Pramono", "Kel. Bapak Agus Mahendra"] },
  },
});
