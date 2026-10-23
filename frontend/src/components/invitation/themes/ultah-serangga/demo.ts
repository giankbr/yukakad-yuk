import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arsya", groom: "",
    brideFull: "Arsya Danendra Prasetyo",
    brideParents: "Putra kedua dari Bapak Galih Prasetyo & Ibu Maya Anggraini",
    note: "Arsya genap lima tahun! Ayo bawa topi, rasa penasaran, dan senyum terbaikmu. Kita berburu kupu-kupu bersama di taman.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-10T15:30:00+07:00",
  place: "Taman Kupu-Kupu Cihanjuang",
  address: "Jl. Cihanjuang No. 9, Cibaligo, Kec. Parongpong, Kabupaten Bandung Barat",
  story: { title: "Cerita Arsya", body: "" },
  stories: [
    { date: "2022", title: "Lahir di musim kupu-kupu", body: "Arsya lahir pagi hari ketika taman depan rumah penuh kupu-kupu kuning. Sejak itu Bunda menyebutnya si penjelajah kecil." },
    { date: "2025", title: "Kaca pembesar pertama", body: "Hadiah dari Kakek ini dibawa ke mana-mana. Semut, daun, dan batu kerikil semuanya diperiksa dengan serius." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Arsya sudah hafal nama sepuluh serangga dan ingin mengenalkan semuanya kepada teman-teman." },
  ],
  events: [
    { name: "Pesta Taman Arsya", date: "2027-07-10T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Taman Kupu-Kupu Cihanjuang", address: "Jl. Cihanjuang No. 9, Cibaligo, Kec. Parongpong, Kabupaten Bandung Barat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 7710 2027", account_name: "Maya Anggraini" },
    { id: "demo-kado", type: "address", address: "Jl. Sersan Bajuri No. 21, Isola, Kec. Sukasari, Kota Bandung 40154" },
  ],
  guestName: "Adik Nadia & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arsya Danendra Prasetyo", nickname: "Arsya", birthDate: "2022-07-08T07:20:00+07:00", parents: "Putra kedua dari Bapak Galih Prasetyo & Ibu Maya Anggraini" },
    rundown: { items: [
      { time: "15.30", title: "Datang & ambil kaca pembesar", note: "Setiap anak dapat satu untuk dibawa pulang" },
      { time: "15.50", title: "Jelajah taman kupu-kupu bersama pemandu" },
      { time: "16.40", title: "Lomba mewarnai kepik dan lebah" },
      { time: "17.20", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju bermotif serangga atau warna cerah kebun: merah, kuning, hijau.", colors: ["#e2412f", "#ffc93c", "#5fae4a", "#a979d6"] },
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Prasetyo", "Abah & Ambu Anggraini", "Kak Salsa"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Arsya impikan.", items: [
      { id: "w1", name: "Buku ensiklopedia serangga anak", price: "± Rp110.000" },
      { id: "w2", name: "Kotak pengamat serangga", price: "± Rp75.000", claimed_by: "Om Fikri" },
      { id: "w3", name: "Sepatu bot hujan hijau", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, ada gazebo teduh untuk orang tua di tengah taman." },
      { q: "Bagaimana jika hujan?", a: "Acara pindah ke rumah kaca di samping taman. Kupu-kupunya tetap ada!" },
    ] },
  },
});
