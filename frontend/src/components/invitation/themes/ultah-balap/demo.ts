import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rafka", groom: "",
    brideFull: "Rafka Alvaro Pratama",
    brideParents: "Putra pertama dari Bapak Dimas Pratama & Ibu Anindya Kusuma",
    note: "Mesin sudah menyala, bendera siap dikibarkan! Rafka genap lima tahun dan mengajak teman-teman balapan di pesta paling seru.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-03-20T15:00:00+07:00",
  place: "Kidz Kart Arena",
  address: "Jl. Terusan Buah Batu No. 77, Batununggal, Bandung Kidul, Kota Bandung",
  story: { title: "Cerita Rafka", body: "" },
  stories: [
    { date: "2022", title: "Start pertama", body: "Rafka lahir di pagi yang cerah, menangis paling kencang di ruang bayi, seperti mesin yang baru dinyalakan." },
    { date: "2024", title: "Brum brum!", body: "Kata favorit pertamanya: brum! Semua benda bulat jadi setir, termasuk tutup panci milik Ibu." },
    { date: "2026", title: "Juara balap sepeda", body: "Di lomba sepeda roda empat TK, Rafka finis kedua dan tetap tersenyum sambil memeluk temannya yang juara." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Rafka hafal semua warna bendera balap dan bercita-cita merancang mobil yang bisa terbang." },
  ],
  events: [
    { name: "Grand Prix Ulang Tahun Rafka", date: "2027-03-20T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Kidz Kart Arena", address: "Jl. Terusan Buah Batu No. 77, Batununggal, Bandung Kidul, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "7730 2251 94", account_name: "Anindya Kusuma" },
    { id: "demo-kado", type: "address", address: "Jl. Batununggal Indah VI No. 18, Bandung Kidul, Kota Bandung 40266" },
  ],
  guestName: "Adik Kiano & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Rafka Alvaro Pratama", nickname: "Rafka", birthDate: "2022-03-20T06:40:00+07:00", parents: "Putra pertama dari Bapak Dimas Pratama & Ibu Anindya Kusuma" },
    rundown: { items: [
      { time: "15.00", title: "Registrasi pembalap cilik", note: "Ambil helm, nomor dada & SIM balap" },
      { time: "15.20", title: "Balap gokar mini & mobil dorong" },
      { time: "16.30", title: "Podium: semua anak dapat medali" },
      { time: "17.00", title: "Tiup lilin, potong kue & bingkisan" },
    ] },
    dressCode: { note: "Kostum tim balap! Merah, biru, atau kotak-kotak hitam putih. Helm kami sediakan.", colors: ["#e63b2e", "#1f7fd6", "#22252d", "#fbf8f0"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Opa & Oma Kusuma", "Kak Alesha (sepupu Rafka)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah paling seru. Kalau ingin memberi, ini yang sedang Rafka impikan.", items: [
      { id: "w1", name: "Set lintasan mobil balap", price: "± Rp250.000" },
      { id: "w2", name: "Buku cerita mobil-mobil", price: "± Rp75.000", claimed_by: "Tante Rara" },
      { id: "w3", name: "Mobil remote control", price: "± Rp300.000" },
    ] },
    faq: { items: [
      { q: "Apakah anak harus bisa menyetir gokar?", a: "Tidak perlu. Gokar mini didampingi kakak marshal dan ada mobil dorong untuk adik yang lebih kecil." },
      { q: "Ada parkir?", a: "Parkir mobil tersedia di halaman Kidz Kart Arena." },
    ] },
  },
});
