import { makeDemo } from "../demo-base";

// Ulang tahun anak bertema polisi cilik di taman lalu lintas: belajar rambu, menyeberang di zebra cross, naik
// mobil patroli mainan, lalu tiup lilin.
export const demo = makeDemo({
  couple: {
    bride: "Arkan", groom: "",
    brideFull: "Muhammad Arkan Pradipta",
    brideParents: "Putra pertama dari Bapak Yoga Pradipta & Ibu Sekar Ayuningtyas",
    note: "Perhatian, perhatian! Semua polisi cilik diminta merapat. Ada patroli seru, rambu-rambu, dan kue ulang tahun yang harus diamankan bersama Arkan.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-06-19T15:30:00+07:00",
  place: "Taman Lalu Lintas Ade Irma Suryani",
  address: "Jl. Belitung No. 1, Merdeka, Kec. Sumur Bandung, Kota Bandung",
  story: { title: "Cerita Arkan", body: "" },
  stories: [
    { date: "2022", title: "Halo dunia!", body: "Arkan lahir di bulan Juni, saat hujan pertama musim kemarau. Suaranya nyaring, kata Bunda seperti peluit." },
    { date: "2025", title: "Hafal warna lampu", body: "Merah berhenti, kuning hati-hati, hijau jalan. Setiap lewat lampu merah, Arkan yang mengingatkan Ayah." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Arkan ingin jadi polisi yang membantu orang menyeberang, dan merayakannya bersama teman-teman." },
  ],
  events: [
    { name: "Patroli Ulang Tahun Arkan", date: "2027-06-19T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Taman Lalu Lintas Ade Irma Suryani", address: "Jl. Belitung No. 1, Merdeka, Kec. Sumur Bandung, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0619 2027 15", account_name: "Sekar Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Jl. Cisitu Indah III No. 12, Dago, Coblong, Kota Bandung 40135" },
  ],
  guestName: "Adik Naura & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Muhammad Arkan Pradipta", nickname: "Arkan", birthDate: "2022-06-15T06:40:00+07:00", parents: "Putra pertama dari Bapak Yoga Pradipta & Ibu Sekar Ayuningtyas" },
    rundown: { items: [
      { time: "15.30", title: "Apel polisi cilik", note: "Setiap anak dapat topi dan lencana bintang" },
      { time: "16.00", title: "Belajar rambu & menyeberang di zebra cross" },
      { time: "16.40", title: "Patroli keliling taman naik mobil mainan" },
      { time: "17.20", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Kaus biru, putih, atau kuning. Boleh pakai kostum polisi cilik!", colors: ["#1d3a6e", "#2f6fd0", "#ffffff", "#ffc93c"] },
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Pradipta", "Opa & Oma Ayuningtyas", "Adik Kinan"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Arkan impikan.", items: [
      { id: "w1", name: "Buku cerita rambu lalu lintas", price: "± Rp75.000" },
      { id: "w2", name: "Set mobil patroli & rambu mainan", price: "± Rp230.000", claimed_by: "Tante Rara" },
      { id: "w3", name: "Sepeda roda empat warna biru", price: "± Rp650.000" },
    ] },
    faq: { items: [
      { q: "Apakah anak perlu membawa sepeda?", a: "Tidak perlu, mobil mainan dan sepeda sudah disediakan di taman." },
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, ada area teduh dan minuman untuk orang tua di dekat panggung." },
    ] },
  },
});
