import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinanti", groom: "Arga",
    brideFull: "Kinanti Putri Maheswari", groomFull: "Argadiansyah Pratama",
    brideParents: "Putri kedua dari\nBapak Hendra Wijaya & Ibu Ratna Sari", groomParents: "Putra sulung dari\nBapak Yohanes Pratama & Ibu Dewi Lestari",
    note: "Kami bertemu di jalur setapak menuju curug, basah kuyup oleh kabut. Sejak itu, setiap perjalanan terasa lebih ringan karena dijalani berdua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T15:00:00+07:00",
  place: "Taman Kabut Curug Cilember",
  address: "Jl. Raya Puncak Gg. Curug Cilember, Jogjogan, Cisarua, Kabupaten Bogor",
  stories: [
    { date: "2019", title: "Jalur Curug", body: "Satu rombongan pendakian, satu jas hujan yang dipinjamkan. Arga pura-pura tidak kedinginan sepanjang jalan pulang." },
    { date: "2022", title: "Sembilan Air Terjun", body: "Kami menargetkan mengunjungi sembilan air terjun dalam setahun. Yang ketujuh ternyata jadi tempat Arga melamar." },
    { date: "2027", title: "Kembali ke Hutan", body: "Kami memilih merayakan hari bahagia di tempat semuanya bermula, ditemani suara air dan orang-orang tersayang." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-09-18T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Dek Kayu Tepi Curug", address: "Kawasan Wisata Curug Cilember, Jogjogan, Cisarua, Bogor" },
    { name: "Resepsi Taman", date: "2027-09-18T16:30:00+07:00", time: "16.30 – 20.00 WIB", venue: "Taman Kabut Curug Cilember", address: "Jl. Raya Puncak Gg. Curug Cilember, Jogjogan, Cisarua, Bogor" },
  ],
  gallery: ["/themes/img/r108.webp", "/themes/img/a117.webp", "/themes/img/a30.webp", "/themes/img/r89.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "8730 4412 96", account_name: "Kinanti Putri Maheswari" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "133 00 2648 1157", account_name: "Argadiansyah Pratama" },
  ],
  guestName: "Sdr. Bimo Hartanto & Partner",
  guestTable: "Meja Pakis",
  extras: {
    rundown: { items: [
      { time: "15.00", title: "Upacara di dek tepi curug", note: "Mohon hadir 15 menit lebih awal" },
      { time: "16.30", title: "Teh sore & kudapan hangat" },
      { time: "18.00", title: "Makan malam di bawah lampu gantung" },
      { time: "19.30", title: "Dansa & api unggun kecil" },
    ] },
    dressCode: { note: "Nuansa hutan: hijau lumut, toska, krem, atau cokelat batu. Gunakan alas kaki yang nyaman untuk jalan tanah.", colors: ["#2f6a36", "#2fb3a8", "#eef2e6", "#5a675f"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Wijaya", "Kel. Besar Bpk. Yohanes Pratama"] },
    travel: { note: "Lokasi ada di jalur Puncak, sebaiknya berangkat pagi untuk menghindari buka-tutup jalan.", items: [
      { name: "Shuttle tamu", detail: "Dari Botani Square pukul 12.30 dan 13.30" },
      { name: "Penginapan", detail: "Beberapa vila di Cisarua, ± 10 menit dari lokasi" },
    ] },
    faq: { items: [
      { q: "Apakah acara di luar ruangan?", a: "Ya, sebagian besar acara di taman terbuka. Kami menyiapkan tenda dan payung bila hujan." },
      { q: "Apakah jalannya menanjak?", a: "Ada jalur setapak ± 150 m dari parkir. Tersedia jalur landai untuk orang tua dan kursi roda." },
    ] },
  },
});
