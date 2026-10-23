import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Damar", groom: "",
    brideFull: "Damar Satria Nugroho",
    brideParents: "Putra kedua dari Bapak Yoga Nugroho & Ibu Larasati Wulandari",
    note: "Tut tut! Kereta pesta segera berangkat. Damar genap lima tahun dan mengajak teman-teman naik ke gerbong paling seru.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-08-21T15:00:00+07:00",
  place: "Aula Taman Bermain Pelangi",
  address: "Jl. Kaliurang Km 7 No. 18, Condongcatur, Depok, Sleman, Yogyakarta",
  story: { title: "Cerita Damar", body: "" },
  stories: [
    { date: "2022", title: "Penumpang baru", body: "Damar lahir di sore yang tenang, tepat saat kereta senja lewat di dekat rumah Eyang." },
    { date: "2024", title: "Tut tut pertama", body: "Kata yang paling sering Damar ucapkan adalah 'tut tut'. Setiap ada suara kereta, ia langsung lari ke jendela." },
    { date: "2026", title: "Rel di ruang tamu", body: "Rel kayu mainan memanjang dari kamar sampai dapur. Damar menjadi masinis, kakaknya kepala stasiun." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Damar hafal warna setiap gerbong dan ingin mengajak semua teman naik kereta pesta." },
  ],
  events: [
    { name: "Pesta Kereta Ulang Tahun Damar", date: "2027-08-21T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Aula Taman Bermain Pelangi", address: "Jl. Kaliurang Km 7 No. 18, Condongcatur, Depok, Sleman, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "0373 5512 84", account_name: "Larasati Wulandari" },
    { id: "demo-kado", type: "address", address: "Jl. Gejayan Gg. Kenari No. 9, Caturtunggal, Depok, Sleman 55281" },
  ],
  guestName: "Adik Naya & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Damar Satria Nugroho", nickname: "Damar", birthDate: "2022-08-21T16:20:00+07:00", parents: "Putra kedua dari Bapak Yoga Nugroho & Ibu Larasati Wulandari" },
    rundown: { items: [
      { time: "15.00", title: "Penumpang naik", note: "Ambil tiket & topi masinis di pintu" },
      { time: "15.20", title: "Lomba menyusun rel kayu" },
      { time: "16.00", title: "Kereta kardus keliling taman" },
      { time: "16.45", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Kostum masinis atau baju warna-warni seperti gerbong: merah, kuning, biru, hijau.", colors: ["#e0483a", "#f6c23e", "#3a7fd0", "#4fb06b"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Nugroho", "Mbah Kakung & Mbah Putri Wulandari", "Mas Bima (kakak Damar)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah paling seru. Kalau ingin memberi, ini yang sedang Damar impikan.", items: [
      { id: "w1", name: "Set rel kayu tambahan", price: "± Rp200.000" },
      { id: "w2", name: "Buku cerita kereta api", price: "± Rp75.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Gerbong mainan magnet", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, tersedia tempat duduk untuk orang tua di sekitar arena." },
      { q: "Ada parkir?", a: "Parkir mobil dan motor tersedia di halaman taman bermain." },
    ] },
  },
});
