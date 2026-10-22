import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Clara", groom: "Adrian",
    brideFull: "Maria Clara Wulandari, S.H.", groomFull: "Adrianus Bayu Setiawan, M.M.",
    brideParents: "Putri bungsu dari\nBapak Yohanes Sutrisno & Ibu Theresia Endang Lestari",
    groomParents: "Putra kedua dari\nBapak Fransiskus Hadi Wibowo & Ibu Agnes Ratna Sari",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Satu lilin tidak berkurang cahayanya ketika menyalakan lilin yang lain. Begitulah kami ingin saling menerangi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T10:00:00+07:00",
  place: "Ruang Jamuan Villa Teratai",
  address: "Jl. Dago Giri No. 88, Mekarwangi, Lembang, Kabupaten Bandung Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Desember 2019", title: "Misa malam Natal", body: "Lilin Clara padam tertiup angin di halaman gereja. Adrian, yang berdiri di sebelahnya, menyalakannya kembali dari lilinnya sendiri." },
    { date: "2020 – 2025", title: "Makan malam setiap Jumat", body: "Dari warung tenda sampai dapur kecil di kos, kami menjaga satu kebiasaan: makan malam bersama setiap Jumat, apa pun yang terjadi minggu itu." },
    { date: "Februari 2027", title: "Lamaran di meja yang sama", body: "Di restoran tempat kencan pertama kami, dengan dua lilin dan sebuah cincin di bawah serbet, Adrian bertanya dan Clara menjawab ya." },
  ],
  events: [
    { name: "Sakramen Perkawinan", date: "2027-10-16T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gereja Katedral Santo Petrus", address: "Jl. Merdeka No. 14, Babakan Ciamis, Sumur Bandung, Kota Bandung" },
    { name: "Jamuan Makan Malam", date: "2027-10-16T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Ruang Jamuan Villa Teratai", address: "Jl. Dago Giri No. 88, Mekarwangi, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/a118.webp", "/themes/img/a86.webp", "/themes/img/a124.webp", "/themes/img/a85.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 6612 85", account_name: "Maria Clara Wulandari" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0198 2257 4", account_name: "Adrianus Bayu Setiawan" },
    { id: "demo-kado", type: "address", address: "Jl. Cisitu Indah III No. 21, Dago, Coblong, Kota Bandung 40135" },
  ],
  guestName: "Ibu Veronika Kristanti & Keluarga",
  guestTable: "Meja Lilin 4",
  extras: {
    quote: { text: "Taruhlah aku seperti meterai pada hatimu, seperti meterai pada lenganmu, karena cinta kuat seperti maut. Air yang banyak tak dapat memadamkan cinta, sungai-sungai tak dapat menghanyutkannya.", source: "Kidung Agung 8:6-7" },
    rundown: { items: [
      { time: "18.30", title: "Sambutan & aperitif", note: "Iringan kuartet gesek" },
      { time: "19.00", title: "Kedatangan kedua mempelai & doa makan" },
      { time: "19.15", title: "Santap malam tiga hidangan" },
      { time: "20.30", title: "Bersulang & potong kue", note: "Dilanjutkan dansa pertama" },
    ] },
    dressCode: { note: "Formal malam: warna anggur, cokelat tua, hitam, atau emas lembut.", colors: ["#5a1622", "#3a2018", "#151010", "#c99a4c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: { label: "Pantangan makanan untuk jamuan (opsional)" },
    family: { names: ["Kel. Besar Yohanes Sutrisno", "Kel. Besar Fransiskus Hadi Wibowo", "Paduan Suara St. Caecilia"] },
    faq: { items: [
      { q: "Apakah tamu dapat menghadiri misa pemberkatan?", a: "Tentu. Mohon datang 15 menit lebih awal dan berpakaian sopan." },
      { q: "Apakah tersedia menu vegetarian?", a: "Tersedia. Cantumkan pada kolom pantangan makanan saat konfirmasi." },
    ] },
  },
});
