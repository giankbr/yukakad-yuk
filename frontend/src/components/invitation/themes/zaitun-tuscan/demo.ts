import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Arya",
    brideFull: "Caecilia Laras Kinanti, S.Gz.", groomFull: "Benedictus Arya Wicaksono, S.T.P.",
    brideParents: "Putri kedua dari\nBapak Yohanes Hadi Prasetyo & Ibu Maria Endang Lestari", groomParents: "Putra sulung dari\nBapak Petrus Agung Wicaksono & Ibu Veronika Sri Rahayu",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Seperti pohon zaitun yang tumbuh perlahan dan berbuah lama, kami ingin cinta ini berakar dalam.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T09:00:00+07:00",
  place: "Rumah Kebun Dago Giri",
  address: "Jl. Dago Giri No. 88, Mekarwangi, Lembang, Bandung Barat",
  stories: [
    { date: "2018", title: "Kelas Pengolahan Pangan", body: "Laras menumpahkan minyak zaitun di meja praktikum Arya. Ia minta maaf, Arya minta resep salad-nya." },
    { date: "2022", title: "Kebun Kecil di Lembang", body: "Kami menanam bibit zaitun dalam pot terakota di teras, dan merawatnya bersama setiap akhir pekan." },
    { date: "2026", title: "Lamaran Sore Hari", body: "Di jalan setapak berpohon cemara, saat matahari sore menguning, Arya berlutut dan Laras menjawab ya." },
  ],
  events: [
    { name: "Misa Sakramen Perkawinan", date: "2027-06-19T09:00:00+07:00", time: "09.00 – 11.00 WIB", venue: "Gereja Katolik Santo Laurentius", address: "Jl. Sukajadi No. 223, Sukagalih, Sukajadi, Bandung" },
    { name: "Resepsi Kebun", date: "2027-06-19T16:00:00+07:00", time: "16.00 – 19.30 WIB", venue: "Rumah Kebun Dago Giri", address: "Jl. Dago Giri No. 88, Mekarwangi, Lembang, Bandung Barat" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/r8.webp", "/themes/img/a111.webp", "/themes/img/r5.webp", "/themes/img/a31.webp", "/themes/img/r104.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5210 7788 14", account_name: "Caecilia Laras Kinanti" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0192 8833 5", account_name: "Benedictus Arya Wicaksono" },
    { id: "demo-kado", type: "address", address: "Jl. Cipaganti No. 51, Coblong, Bandung 40131" },
  ],
  guestName: "Ibu Theresia Wulandari & Keluarga",
  guestTable: "Meja Zaitun 4",
  extras: {
    quote: { text: "Isterimu akan menjadi seperti pohon anggur yang subur di dalam rumahmu; anak-anakmu seperti tunas pohon zaitun sekeliling mejamu.", source: "Mazmur 128:3" },
    rundown: { items: [
      { time: "16.00", title: "Aperitivo & penyambutan", note: "Teras kebun" },
      { time: "16.45", title: "Kirab mempelai di jalan cemara" },
      { time: "17.30", title: "Makan malam panjang di meja kayu" },
      { time: "18.45", title: "Potong kue & dansa pertama" },
    ] },
    dressCode: { note: "Nuansa pedesaan sore: hijau sage, terakota, krem, dan zaitun.", colors: ["#8c9468", "#b8603f", "#efe2c8", "#5d6b45"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Yohanes Hadi Prasetyo", "Kel. Besar Bpk. Petrus Agung Wicaksono"] },
  },
});
