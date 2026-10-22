import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Mayang", groom: "Rendra",
    brideFull: "Mayang Kusuma Wardhani",
    groomFull: "Rendra Adiputra Santoso",
    brideParents: "Putri dari Bapak Hendro Wardhana & Ibu Ratna Kusumawati",
    groomParents: "Putra dari Bapak Agus Santoso & Ibu Lina Marlina",
    bridePhoto: "/themes/img/a77.webp",
    groomPhoto: "/themes/img/a76.webp",
    note: "Tujuh tahun berteman, tiga tahun bersama. Sekarang kami ingin mengikatnya dengan sebuah janji kecil, di depan orang-orang yang paling kami sayangi.",
  },
  eventLabel: "Tunangan",
  date: "2027-05-22T16:00:00+07:00",
  place: "Ruang Teras, Kinara Hall",
  address: "Jl. Senopati No. 41, Selong, Kebayoran Baru, Jakarta Selatan",
  story: { title: "Cerita singkat", body: "" },
  stories: [
    { date: "2020", title: "Satu meja kerja", body: "Bertemu di proyek pameran arsitektur. Mayang menggambar denahnya, Rendra yang selalu salah membaca skalanya." },
    { date: "2024", title: "Pulang bersama", body: "Dari teman satu tim menjadi teman perjalanan, lalu teman pulang setiap Jumat sore." },
    { date: "2027", title: "Satu pertanyaan", body: "Ditanyakan di bawah pohon pinus, dijawab dengan tawa dan satu kata: iya." },
  ],
  events: [
    { name: "Pertukaran Cincin", date: "2027-05-22T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Ruang Teras, Kinara Hall", address: "Jl. Senopati No. 41, Selong, Kebayoran Baru, Jakarta Selatan" },
    { name: "Makan Malam Bersama", date: "2027-05-22T18:00:00+07:00", time: "18.00 – 20.00 WIB", venue: "Ruang Kaca, Kinara Hall", address: "Jl. Senopati No. 41, Selong, Kebayoran Baru, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a74.webp", "/themes/img/r89.webp", "/themes/img/a77.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5271 0098 31", account_name: "Mayang Kusuma Wardhani" },
  ],
  guestName: "Sdr. Bayu Pratama",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "16.00", title: "Penyambutan kedua keluarga" },
      { time: "16.20", title: "Kata pengantar & doa" },
      { time: "16.40", title: "Pertukaran cincin" },
      { time: "18.00", title: "Makan malam & foto bersama" },
    ] },
    dressCode: { note: "Putih, gading, atau abu-abu. Satu aksen terakota dipersilakan.", colors: ["#f5f3ef", "#d9d4cb", "#6e6a63", "#b9562f"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Bersama keluarga", names: ["Keluarga Bapak Hendro Wardhana", "Keluarga Bapak Agus Santoso"] },
    faq: { items: [
      { q: "Apakah acaranya terbuka untuk umum?", a: "Acara ini terbatas untuk keluarga dan sahabat dekat. Mohon konfirmasi kehadiran sebelum 15 Mei." },
      { q: "Tersedia parkir?", a: "Tersedia parkir di basement Kinara Hall, masuk dari Jl. Senopati." },
    ] },
  },
});
