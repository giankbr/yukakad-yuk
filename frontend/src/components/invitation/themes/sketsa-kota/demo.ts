import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Damar",
    brideFull: "Kirana Putri Larasati, S.Ars.", groomFull: "Damar Wicaksono, S.Ds.",
    brideParents: "Putri kedua dari\nBapak Hendro Wibisono & Ibu Lestari Handayani", groomParents: "Putra sulung dari\nBapak Antonius Setiadi & Ibu Maria Kristiani",
    bridePhoto: "/themes/img/a114.webp", groomPhoto: "/themes/img/r71.webp",
    note: "Kami bertemu di sebuah pojok jalan tua, sama-sama duduk di trotoar dengan buku sketsa. Sejak itu, setiap kota terasa lebih indah digambar berdua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T16:00:00+07:00",
  place: "Galeri Rumah Lawas",
  address: "Jl. Letjen Suprapto No. 31, Tanjung Mas, Semarang Utara, Kota Semarang",
  stories: [
    { date: "2020", title: "Sketchwalk Pertama", body: "Kirana menggambar menara jam, Damar menggambar Kirana yang sedang menggambar. Ketahuan, lalu kami tertawa dan bertukar nomor." },
    { date: "2023", title: "Satu Buku, Dua Tangan", body: "Kami mulai mengisi satu buku sketsa berdua: Kirana menarik garis, Damar memberi warna. Sudah tiga buku penuh sampai hari ini." },
    { date: "2026", title: "Di Bawah Lampu Jalan", body: "Di pojok jalan yang sama, Damar membuka halaman terakhir buku ketiga. Isinya satu pertanyaan, dan jawabannya: iya." },
  ],
  events: [
    { name: "Pemberkatan & Janji Nikah", date: "2027-05-22T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Galeri Rumah Lawas", address: "Jl. Letjen Suprapto No. 31, Tanjung Mas, Semarang Utara, Kota Semarang" },
    { name: "Resepsi Taman", date: "2027-05-22T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Halaman Belakang Rumah Lawas", address: "Jl. Letjen Suprapto No. 31, Tanjung Mas, Semarang Utara, Kota Semarang" },
  ],
  gallery: ["/themes/img/a100.webp", "/themes/img/r56.webp", "/themes/img/r7.webp", "/themes/img/r6.webp", "/themes/img/r70.webp", "/themes/img/r63.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0095 6612 30", account_name: "Kirana Putri Larasati" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0817 4421 9033", account_name: "Damar Wicaksono" },
    { id: "demo-kado", type: "address", address: "Jl. Kepodang No. 12, Purwodinatan, Semarang Tengah, Kota Semarang 50137" },
  ],
  guestName: "Mbak Sekar & Partner",
  guestTable: "Meja Sketsa 4",
  extras: {
    quote: { text: "Kota-kota berubah, gedung dicat ulang, jalan diganti nama. Tapi pojok tempat kita pertama bertemu akan selalu tergambar sama.", source: "Catatan di halaman belakang buku sketsa kami" },
    rundown: { items: [
      { time: "16.00", title: "Janji nikah", note: "Keluarga & sahabat dekat" },
      { time: "18.30", title: "Resepsi taman dibuka" },
      { time: "19.15", title: "Pameran mini sketsa kami", note: "Bawa pulang satu kartu pos" },
      { time: "20.00", title: "Makan malam & musik akustik" },
    ] },
    dressCode: { note: "Santai rapi nuansa warna cat air: terakota, oker, hijau toska, dan biru langit. Sepatu nyaman, halaman berlantai batu.", colors: ["#c0674a", "#e7bf7f", "#4f8f8a", "#9cc3dc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Bpk. Hendro Wibisono", "Kel. Bpk. Antonius Setiadi", "Teman-teman Komunitas Sketsa Semarang"] },
  },
});
