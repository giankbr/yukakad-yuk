import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    note: "Hore, Arka sudah tujuh tahun! Ayo rayakan bersama dengan balon, kue, dan banyak tawa.",
    brideFull: "Arkana Putra Mahendra",
    brideParents: "Putra pertama dari Bapak Dimas Mahendra & Ibu Laras Ayu",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-03-14T15:00:00+07:00",
  place: "Aula Taman Bermain Pelangi",
  address: "Jl. Kemang Raya No. 18, Mampang Prapatan, Jakarta Selatan",
  story: { title: "Cerita Arka", body: "" },
  stories: [
    { date: "2020", title: "Halo dunia!", body: "Arka lahir di pagi yang cerah, membawa tangis pertama yang paling ditunggu Ayah dan Bunda." },
    { date: "2023", title: "Hari pertama sekolah", body: "Masuk kelompok bermain dengan tas dinosaurus kesayangan dan langsung punya tiga sahabat baru." },
    { date: "2026", title: "Bisa naik sepeda", body: "Setelah jatuh bangun berkali-kali, akhirnya roda bantu sepeda boleh dilepas." },
    { date: "2027", title: "Tujuh tahun!", body: "Sekarang Arka suka menggambar roket, membaca buku dinosaurus, dan membantu Bunda menyiram tanaman." },
  ],
  events: [
    { name: "Pesta Ulang Tahun", date: "2027-03-14T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Aula Taman Bermain Pelangi", address: "Jl. Kemang Raya No. 18, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5210 3344 87", account_name: "Laras Ayu Pratiwi" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka XI No. 7, Pela Mampang, Jakarta Selatan 12720" },
  ],
  guestName: "Kakak Naura & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arkana Putra Mahendra", nickname: "Arka", birthDate: "2020-03-14T07:30:00+07:00", parents: "Putra pertama dari Bapak Dimas Mahendra & Ibu Laras Ayu" },
    rundown: { items: [
      { time: "15.00", title: "Kedatangan & photo booth", note: "Ambil topi pesta di meja depan" },
      { time: "15.30", title: "Sulap & badut lucu" },
      { time: "16.15", title: "Tiup lilin & potong kue", note: "Nyanyi bersama" },
      { time: "16.45", title: "Lomba & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju warna cerah, boleh kostum dinosaurus atau astronot.", colors: ["#ff6b6b", "#ffc93c", "#4ecdc4", "#8e7dff"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Mahendra", "Opa & Oma Pratiwi", "Om Bayu & Tante Sinta"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi kado terindah. Kalau ingin memberi, ini daftar kesukaan Arka.", items: [
      { id: "w1", name: "Buku ensiklopedia dinosaurus", price: "± Rp150.000" },
      { id: "w2", name: "Set krayon & buku gambar", price: "± Rp90.000", claimed_by: "Tante Sinta" },
      { id: "w3", name: "Mainan roket balok susun", price: "± Rp250.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada area duduk dan camilan untuk Ayah & Bunda." },
      { q: "Ada area parkir?", a: "Tersedia parkir di halaman aula dan sepanjang Jl. Kemang Raya." },
    ] },
  },
});
