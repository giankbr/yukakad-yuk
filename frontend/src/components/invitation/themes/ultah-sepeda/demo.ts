import { makeDemo } from "../demo-base";

// Ulang tahun anak bertema sepeda: gowes bareng di taman lalu lintas, helm warna-warni, cone, bendera, dan balon.
export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    brideFull: "Arkananta Bima Saputra",
    brideParents: "Putra pertama dari Bapak Dimas Saputra & Ibu Anindya Paramitha",
    note: "Arka sudah bisa gowes tanpa roda bantu! Bawa sepeda dan helmmu, kita keliling lintasan sama-sama.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-05-16T08:30:00+07:00",
  place: "Taman Lalu Lintas Ade Irma Suryani",
  address: "Jl. Belitung No. 1, Merdeka, Kec. Sumur Bandung, Kota Bandung",
  story: { title: "Cerita Gowes Arka", body: "" },
  stories: [
    { date: "2021", title: "Halo dunia", body: "Arka lahir di bulan Mei, kecil dan suka menendang-nendang seperti sedang mengayuh." },
    { date: "2024", title: "Sepeda roda tiga", body: "Sepeda merah pertama, dikayuh keliling teras sampai ban belakangnya botak." },
    { date: "2026", title: "Roda bantu dilepas", body: "Jatuh dua kali, bangun tiga kali, lalu meluncur sendiri sambil teriak memanggil Ayah." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang hafal rambu lalu lintas dan selalu mengingatkan Bunda memakai helm." },
  ],
  events: [
    { name: "Gowes Bareng Arka", date: "2027-05-16T08:30:00+07:00", time: "08.30 – 11.30 WIB", venue: "Taman Lalu Lintas Ade Irma Suryani", address: "Jl. Belitung No. 1, Merdeka, Kec. Sumur Bandung, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1300 0215 6620 9", account_name: "Anindya Paramitha" },
    { id: "demo-kado", type: "address", address: "Jl. Sukaluyu No. 22, Cibeunying Kaler, Kota Bandung 40123" },
  ],
  guestName: "Adik Naufal & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arkananta Bima Saputra", nickname: "Arka", birthDate: "2021-05-16T07:10:00+07:00", parents: "Putra pertama dari Bapak Dimas Saputra & Ibu Anindya Paramitha" },
    quote: { text: "Hidup itu seperti naik sepeda. Supaya tetap seimbang, kamu harus terus bergerak.", source: "Albert Einstein" },
    rundown: { items: [
      { time: "08.30", title: "Cek helm & pasang nomor dada", note: "Helm cadangan tersedia untuk yang lupa" },
      { time: "09.00", title: "Gowes keliling lintasan", note: "Didampingi kakak pemandu" },
      { time: "10.00", title: "Lomba lambat-lambatan & zig-zag cone" },
      { time: "10.45", title: "Tiup lilin & makan bersama" },
    ] },
    dressCode: { note: "Baju olahraga yang nyaman dan sepatu tertutup. Jangan lupa helm!", colors: ["#ff6b4a", "#ffc93c", "#1fa4a0", "#5fb8e8"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Saputra", "Opa & Oma Paramitha"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Arka.", items: [
      { id: "w1", name: "Bel sepeda bentuk dinosaurus", price: "± Rp45.000" },
      { id: "w2", name: "Lampu sepeda depan-belakang", price: "± Rp90.000", claimed_by: "Om Reza" },
      { id: "w3", name: "Sarung tangan sepeda anak", price: "± Rp75.000" },
    ] },
    faq: { items: [
      { q: "Belum punya sepeda, boleh ikut?", a: "Boleh! Taman menyewakan sepeda anak, dan kami siapkan beberapa untuk dipinjam." },
      { q: "Apakah orang tua boleh ikut?", a: "Tentu, ada tempat duduk teduh di pinggir lintasan untuk Ayah dan Bunda." },
    ] },
  },
});
