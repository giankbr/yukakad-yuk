import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kayla", groom: "",
    brideFull: "Kayla Putri Samudera",
    brideParents: "Putri kedua dari Bapak Rizky Pratama & Ibu Anindya Larasati",
    note: "Ember sudah siap, sekop sudah siap, istana pasir menunggu! Ayo main ombak bersama Kayla.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-06-19T15:30:00+07:00",
  place: "Pantai Lagoon Ancol",
  address: "Taman Impian Jaya Ancol, Jl. Lodan Timur No. 7, Pademangan, Jakarta Utara",
  story: { title: "", body: "" },
  stories: [
    { date: "2022", title: "Bayi musim kemarau", body: "Kayla lahir di bulan Juni yang cerah, saat langit Jakarta sedang biru-birunya." },
    { date: "2025", title: "Kaki pertama di pasir", body: "Di Pantai Anyer, Kayla tertawa setiap kali ombak kecil menggelitik jari kakinya." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Kayla jago membangun istana pasir dan selalu menyapa kepiting yang lewat." },
  ],
  events: [
    { name: "Pesta Pantai Kayla", date: "2027-06-19T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Pantai Lagoon Ancol", address: "Taman Impian Jaya Ancol, Jl. Lodan Timur No. 7, Pademangan, Jakarta Utara" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "122 00 7715 8890", account_name: "Anindya Larasati" },
    { id: "demo-kado", type: "address", address: "Jl. Pluit Karang Indah Timur No. 23, Pluit, Penjaringan, Jakarta Utara 14450" },
  ],
  guestName: "Adik Naufal & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kayla Putri Samudera", nickname: "Kayla", birthDate: "2022-06-19T09:15:00+07:00", parents: "Putri kedua dari Bapak Rizky Pratama & Ibu Anindya Larasati" },
    rundown: { items: [
      { time: "15.30", title: "Lomba istana pasir", note: "Ember & sekop disediakan" },
      { time: "16.15", title: "Main bola pantai & berburu kerang" },
      { time: "17.00", title: "Tiup lilin & potong kue ombak", note: "Nyanyi bersama" },
      { time: "17.30", title: "Bagi-bagi bingkisan" },
    ] },
    dressCode: { note: "Baju pantai yang ceria: warna koral, kuning, toska, atau putih. Jangan lupa topi dan sandal!", colors: ["#ff6f5e", "#ffc93c", "#29b0c2", "#fff4dc"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Opa & Oma Larasati", "Kakak Rafa (kakak Kayla)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini kesukaan Kayla.", items: [
      { id: "w1", name: "Set cetakan istana pasir", price: "± Rp95.000" },
      { id: "w2", name: "Buku cerita hewan pantai", price: "± Rp75.000", claimed_by: "Tante Sari" },
      { id: "w3", name: "Topi pantai anak", price: "± Rp60.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada gazebo teduh dengan kelapa muda untuk Ayah & Bunda." },
      { q: "Perlu membawa baju ganti?", a: "Sangat disarankan, karena anak-anak pasti main air dan pasir." },
    ] },
  },
});
