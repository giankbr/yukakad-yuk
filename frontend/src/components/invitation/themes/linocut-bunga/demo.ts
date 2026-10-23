import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Wulan", groom: "Gema",
    brideFull: "Wulan Kinasih Pertiwi, S.Sn.", groomFull: "Gema Arunika Saputra, S.Ds.",
    brideParents: "Putri kedua dari\nBapak Hendro Wibisono & Ibu Ratna Sulistyowati", groomParents: "Putra sulung dari\nBapak Johan Saputra & Ibu Maria Lestiani",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Dua warna, satu cetakan: yang paling indah justru lahir dari tangan yang mau bekerja bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T10:00:00+07:00",
  place: "Kebun Studio Cikapundung",
  address: "Jl. Siliwangi No. 21, Cipaganti, Coblong, Kota Bandung",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Maret 2021", title: "Kelas Cukil Lino", body: "Satu meja kerja, satu rol tinta yang harus dipakai bergantian. Gema terlalu banyak tinta, Wulan terlalu sedikit." },
    { date: "2023", title: "Pameran Pertama", body: "Kami memamerkan seri cetak bunga liar berdua di sebuah kafe kecil di Dago. Terjual tiga lembar, kami rayakan dengan semangkuk bakso." },
    { date: "Desember 2026", title: "Lembar Lamaran", body: "Gema mencetak satu lembar khusus: bunga madat merah dengan tulisan kecil di pojoknya. Wulan menjawab di lembar yang sama." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-06-19T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Kebun Studio Cikapundung", address: "Jl. Siliwangi No. 21, Cipaganti, Coblong, Kota Bandung" },
    { name: "Resepsi Taman", date: "2027-06-19T16:00:00+07:00", time: "16.00 – 20.00 WIB", venue: "Kebun Studio Cikapundung", address: "Jl. Siliwangi No. 21, Cipaganti, Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a74.webp", "/themes/img/a77.webp", "/themes/img/r88.webp", "/themes/img/a26.webp", "/themes/img/r55.webp", "/themes/img/a76.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "772 091 4410", account_name: "Wulan Kinasih Pertiwi" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2044 7186", account_name: "Gema Arunika Saputra" },
    { id: "demo-kado", type: "address", address: "Studio Rol Merah, Jl. Bukit Dago Utara No. 7, Coblong, Bandung 40135" },
  ],
  guestName: "Ibu Nadia Prameswari & Keluarga",
  guestTable: "Meja Madat 4",
  extras: {
    quote: { text: "Cinta tidak saling menatap, tetapi bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Keluarga & sahabat dekat" },
      { time: "16.00", title: "Resepsi taman dibuka" },
      { time: "17.00", title: "Cetak bersama", note: "Tamu mencetak kartu lino kenang-kenangan" },
      { time: "18.30", title: "Makan malam & musik akustik" },
    ] },
    dressCode: { note: "Krem, merah bata, dan hitam. Bahan katun dan linen sangat cocok untuk taman.", colors: ["#f2e8d5", "#b3271f", "#1d1a17", "#8c7b65"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Apakah acara di luar ruangan?", a: "Ya, resepsi di taman berpayung tenda. Sepatu datar akan lebih nyaman di rumput." },
      { q: "Apa itu sesi cetak bersama?", a: "Kami menyiapkan blok lino kecil. Setiap tamu bisa mencetak kartu bunga sendiri untuk dibawa pulang." },
    ] },
  },
});
