import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "",
    brideFull: "Kirana Ayudia Putri",
    brideParents: "Putri kedua dari Bapak Arif Setiawan & Ibu Nadia Prameswari",
    note: "Sepatu balet sudah dipakai, tutu sudah mengembang. Kirana genap enam tahun dan ingin menari bersama teman-teman!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-05-15T15:30:00+07:00",
  place: "Studio Tari Sekar Arum",
  address: "Jl. Dharmahusada Indah Barat II No. 12, Mulyorejo, Kota Surabaya",
  story: { title: "Cerita Kirana", body: "" },
  stories: [
    { date: "2021", title: "Lahir di bulan Mei", body: "Kirana lahir di pagi yang cerah, kakinya sudah menendang-nendang seperti sedang menari." },
    { date: "2024", title: "Kotak musik dari Eyang", body: "Hadiah ulang tahun ketiga: kotak musik dengan penari kecil yang berputar. Kirana menirukannya setiap malam sebelum tidur." },
    { date: "2026", title: "Kelas balet pertama", body: "Memakai tutu merah muda dan sepatu balet pertama, Kirana belajar plié dan berputar tanpa jatuh." },
    { date: "2027", title: "Enam tahun!", body: "Kini Kirana sudah hafal satu tarian pendek dan ingin menampilkannya untuk teman-teman di hari ulang tahunnya." },
  ],
  events: [
    { name: "Pesta Balet Kirana", date: "2027-05-15T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Studio Tari Sekar Arum", address: "Jl. Dharmahusada Indah Barat II No. 12, Mulyorejo, Kota Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0823 4417 90", account_name: "Nadia Prameswari" },
    { id: "demo-kado", type: "address", address: "Jl. Kalijudan Indah VII No. 34, Mulyorejo, Kota Surabaya 60114" },
  ],
  guestName: "Adik Shakira & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kirana Ayudia Putri", nickname: "Kirana", birthDate: "2021-05-15T07:20:00+07:00", parents: "Putri kedua dari Bapak Arif Setiawan & Ibu Nadia Prameswari" },
    rundown: { items: [
      { time: "15.30", title: "Ganti kostum", note: "Tutu & mahkota bunga disiapkan untuk semua penari kecil" },
      { time: "16.00", title: "Kelas balet mini bersama Kak Laras" },
      { time: "16.45", title: "Pertunjukan kecil Kirana" },
      { time: "17.15", title: "Tiup lilin, potong kue & bingkisan" },
    ] },
    dressCode: { note: "Gaun atau tutu warna merah muda, putih, atau krem. Sepatu boleh dilepas saat menari.", colors: ["#f6bccb", "#fffafb", "#f3d9b8", "#d9617f"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Setiawan", "Oma & Opa Prameswari", "Kak Dimas (kakak Kirana)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Kirana impikan.", items: [
      { id: "w1", name: "Buku cerita balet bergambar", price: "± Rp120.000" },
      { id: "w2", name: "Kotak perhiasan musik", price: "± Rp180.000", claimed_by: "Tante Rina" },
      { id: "w3", name: "Set jepit rambut & bando", price: "± Rp75.000" },
    ] },
    faq: { items: [
      { q: "Apakah anak laki-laki boleh ikut menari?", a: "Tentu! Kelas balet mini untuk semua teman Kirana." },
      { q: "Apakah orang tua ikut masuk?", a: "Ada kursi penonton untuk Ayah & Bunda di belakang studio." },
    ] },
  },
});
