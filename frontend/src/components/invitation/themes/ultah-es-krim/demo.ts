import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alea", groom: "",
    brideFull: "Alea Kinanti Prasetyo",
    brideParents: "Putri pertama dari Bapak Gilang Prasetyo & Ibu Nadia Puspitasari",
    note: "Alea genap lima tahun! Ayo datang, kita tumpuk es krim setinggi-tingginya dan tabur meses warna-warni bersama.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-17T15:30:00+07:00",
  place: "Kedai Es Krim Sundae Sore",
  address: "Jl. Bintaro Utama 3A No. 18, Pondok Karya, Pondok Aren, Tangerang Selatan",
  story: { title: "Cerita Alea", body: "" },
  stories: [
    { date: "2022", title: "Hadiah musim kemarau", body: "Alea lahir di siang yang terik. Kata Ayah, sejak itu rumah kami tak pernah kehabisan es krim di kulkas." },
    { date: "2025", title: "Suapan pertama", body: "Es krim stroberi pertama Alea berakhir di pipi, hidung, dan baju. Tapi senyumnya tidak terlupakan." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Alea sudah bisa memilih rasa sendiri: stroberi, mint, dan cokelat dengan ceri di atasnya." },
  ],
  events: [
    { name: "Pesta Es Krim Alea", date: "2027-07-17T15:30:00+07:00", time: "15.30 – 17.30 WIB", venue: "Kedai Es Krim Sundae Sore", address: "Jl. Bintaro Utama 3A No. 18, Pondok Karya, Pondok Aren, Tangerang Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1270 0717 2027", account_name: "Nadia Puspitasari" },
    { id: "demo-kado", type: "address", address: "Jl. Kenari Raya Blok J2 No. 7, Bintaro Jaya Sektor 9, Tangerang Selatan 15229" },
  ],
  guestName: "Adik Rafi & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Alea Kinanti Prasetyo", nickname: "Alea", birthDate: "2022-07-12T11:20:00+07:00", parents: "Putri pertama dari Bapak Gilang Prasetyo & Ibu Nadia Puspitasari" },
    rundown: { items: [
      { time: "15.30", title: "Datang & ambil celemek mini", note: "Setiap anak dapat topi koki es krim" },
      { time: "15.50", title: "Menghias cone sendiri", note: "Meses, ceri, dan saus stroberi" },
      { time: "16.30", title: "Lomba menara es krim tertinggi" },
      { time: "17.00", title: "Tiup lilin, potong kue es krim & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju warna es krim kesukaanmu: stroberi, mint, vanila, atau cokelat!", colors: ["#f29bb4", "#9fdcc6", "#fbefc8", "#7a4a33", "#b48ce0"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi susu, kacang, atau makanan lain pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Prasetyo", "Opa & Oma Puspitasari"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini yang sedang Alea impikan.", items: [
      { id: "w1", name: "Mainan kedai es krim kayu", price: "± Rp180.000" },
      { id: "w2", name: "Buku cerita bergambar", price: "± Rp75.000", claimed_by: "Tante Rini" },
      { id: "w3", name: "Botol minum karakter", price: "± Rp90.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu. Ada meja dan kursi untuk orang tua di teras kedai, lengkap dengan kopi dan teh." },
      { q: "Ada pilihan untuk anak yang alergi susu?", a: "Ada! Kami menyiapkan sorbet buah tanpa susu. Mohon tuliskan di form konfirmasi." },
    ] },
  },
});
