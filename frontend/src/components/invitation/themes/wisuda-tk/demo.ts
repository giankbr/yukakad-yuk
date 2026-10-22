import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "",
    brideFull: "Kirana Ayu Lestari",
    brideParents: "Putri pertama dari Bapak Yoga Prasetyo & Ibu Mega Lestari",
    note: "Dua tahun bermain, bernyanyi, dan belajar di TK Pelangi Ceria. Sekarang Kirana siap melangkah ke SD!",
  },
  eventLabel: "Pelepasan TK",
  date: "2027-06-19T08:30:00+07:00",
  place: "Aula TK Pelangi Ceria",
  address: "Jl. Kenanga No. 12, Sukaluyu, Cibeunying Kaler, Bandung",
  story: { title: "Cerita Kirana di TK", body: "" },
  stories: [
    { date: "Juli 2025", title: "Hari pertama sekolah", body: "Datang sambil menggenggam tangan Bunda, pulang sudah punya tiga teman baru." },
    { date: "Desember 2025", title: "Pentas tari pertama", body: "Menari Jaipong di panggung pentas akhir semester. Gugup, tapi senyumnya paling lebar." },
    { date: "Februari 2027", title: "Bisa membaca sendiri", body: "Buku cerita kancil kini dibaca sendiri sebelum tidur, lengkap dengan suara-suaranya." },
    { date: "Juni 2027", title: "Lulus TK B", body: "Toga mini sudah dicoba di rumah. Katanya, tali kuningnya paling keren." },
  ],
  events: [
    { name: "Pelepasan & Wisuda TK B", date: "2027-06-19T08:30:00+07:00", time: "08.30 – 11.00 WIB", venue: "Aula TK Pelangi Ceria", address: "Jl. Kenanga No. 12, Sukaluyu, Cibeunying Kaler, Bandung" },
    { name: "Syukuran Kecil di Rumah", date: "2027-06-19T12:30:00+07:00", time: "12.30 – 15.00 WIB", venue: "Kediaman Keluarga Prasetyo", address: "Jl. Cigadung Raya Barat No. 7, Cibeunying Kaler, Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 4471 92", account_name: "Mega Lestari" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Barat No. 7, Cibeunying Kaler, Bandung 40191" },
  ],
  guestName: "Ibu Guru Ratna & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kirana Ayu Lestari", nickname: "Kirana", birthDate: "2021-03-14T07:20:00+07:00", parents: "Putri pertama dari Bapak Yoga Prasetyo & Ibu Mega Lestari" },
    rundown: { items: [
      { time: "08.30", title: "Kirab wisudawan cilik", note: "Masuk aula bersama Bu Guru" },
      { time: "09.00", title: "Penyerahan ijazah & pemindahan tali toga" },
      { time: "09.45", title: "Pentas lagu & tari kelas TK B" },
      { time: "10.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Warna-warni krayon! Merah, biru, kuning, atau hijau. Batik anak juga boleh.", colors: ["#e0483a", "#3a68c2", "#f6c431", "#58a845"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut berbahagia", names: ["Eyang Kakung & Eyang Putri Prasetyo", "Opa & Oma Lestari", "Dek Raka (adik Kirana)"] },
    wishlist: { note: "Kehadiran Bapak/Ibu sudah jadi hadiah terindah. Kalau ingin memberi, ini perlengkapan SD Kirana.", items: [
      { id: "w1", name: "Tas sekolah ransel", price: "± Rp250.000" },
      { id: "w2", name: "Set krayon & buku gambar", price: "± Rp85.000", claimed_by: "Tante Sari" },
      { id: "w3", name: "Botol minum & kotak bekal", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Apakah adik dan kakak boleh ikut?", a: "Boleh sekali. Ada pojok mewarnai untuk anak-anak di belakang aula." },
      { q: "Di mana parkirnya?", a: "Parkir motor di halaman TK, mobil di sepanjang Jl. Kenanga." },
    ] },
  },
});
