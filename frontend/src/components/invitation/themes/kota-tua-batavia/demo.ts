import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Amira", groom: "Fikri",
    brideFull: "Amira Salsabila Sanusi, S.Hum.", groomFull: "Muhammad Fikri Ramadhan, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Mahmud Sanusi & Ibu Hj. Rohayati", groomParents: "Putra pertama dari\nBapak H. Saiful Anwar & Ibu Hj. Nurlela",
    bridePhoto: "/themes/img/r40.webp", groomPhoto: "/themes/img/r41.webp",
    note: "Berawal dari sepeda onthel sewaan dan sore yang terlalu cepat berlalu di alun-alun Kota Tua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T08:00:00+07:00",
  place: "Balai Societeit Kali Besar",
  address: "Jl. Kali Besar Timur No. 9, Pinangsia, Taman Sari, Jakarta Barat",
  stories: [
    { date: "Agustus 2021", title: "Sepeda Onthel Merah", body: "Amira, pemandu wisata sejarah, menyewakan sepeda terakhir di alun-alun kepada Fikri yang datang memotret gedung-gedung tua." },
    { date: "2023", title: "Surat-surat dari Bandung", body: "Fikri bekerja di Bandung. Setiap bulan Amira menerima kartu pos bergambar gedung tua, lengkap dengan perangko dan cap pos." },
    { date: "Februari 2027", title: "Lamaran di Rumah Kemayoran", body: "Rombongan keluarga Fikri datang membawa roti buaya dan palang pintu, disambut pantun dan tawa keluarga Amira." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Jami' An-Nur Pekojan", address: "Jl. Pekojan Raya No. 32, Pekojan, Tambora, Jakarta Barat" },
    { name: "Resepsi", date: "2027-06-19T15:30:00+07:00", time: "15.30 – 19.00 WIB", venue: "Balai Societeit Kali Besar", address: "Jl. Kali Besar Timur No. 9, Pinangsia, Taman Sari, Jakarta Barat" },
  ],
  gallery: ["/themes/img/a100.webp", "/themes/img/r70.webp", "/themes/img/a31.webp", "/themes/img/r64.webp", "/themes/img/r56.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 4488 19", account_name: "Amira Salsabila Sanusi" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5260 1137 02", account_name: "Muhammad Fikri Ramadhan" },
    { id: "demo-kado", type: "address", address: "Jl. Kemayoran Gempol No. 17, Kebon Kosong, Kemayoran, Jakarta Pusat 10630" },
  ],
  guestName: "Bapak H. Zulkifli & Keluarga",
  guestTable: "Meja Onthel 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan hidup dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "15.30", title: "Penyambutan tamu & musik keroncong", note: "Teras depan balai" },
      { time: "16.00", title: "Kirab pengantin bersepeda onthel", note: "Mengelilingi alun-alun" },
      { time: "16.45", title: "Santap sore: kerak telor, soto Betawi, es selendang mayang" },
      { time: "18.00", title: "Foto bersama di bawah lampu jalan" },
    ] },
    dressCode: { note: "Nuansa kartu pos tempo dulu: krem, terakota, hijau jendela, dan cokelat sepia. Kebaya encim dan baju sadariah sangat dipersilakan.", colors: ["#f0e2c4", "#b9573a", "#5d8676", "#6b4a35"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Mahmud Sanusi", "Kel. Besar H. Saiful Anwar", "Komunitas Sepeda Onthel Batavia"] },
    travel: { note: "Kawasan Kota Tua ramai di sore hari. Disarankan datang dengan kereta atau TransJakarta.", items: [
      { name: "KRL & TransJakarta", detail: "Stasiun Jakarta Kota, jalan kaki ± 7 menit" },
      { name: "Parkir", detail: "Gedung parkir Kali Besar Barat, tarif flat" },
    ] },
  },
});
