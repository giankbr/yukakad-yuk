import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Kevin",
    brideFull: "Nadia Paramitha Wijaya", groomFull: "Kevin Adrian Santoso",
    brideParents: "Putri dari Bapak Hendra Wijaya\n& Ibu Lidya Kurniawati", groomParents: "Putra dari Bapak Robert Santoso\n& Ibu Melinda Hartono",
    note: "Satu goresan bisa ragu, dua goresan jadi cerita. Kami memilih menulis sisa halaman ini bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T16:00:00+07:00",
  place: "Galeri Tujuh Rooftop",
  address: "Jl. Senopati No. 77, Selong, Kebayoran Baru, Jakarta Selatan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2021", title: "Kelas Kaligrafi Kuas", body: "Kami duduk bersebelahan di kelas lettering akhir pekan. Tinta Kevin tumpah ke kertas Nadia, dan permintaan maafnya berlanjut jadi kopi." },
    { date: "2023", title: "Pameran Pertama", body: "Nadia memamerkan karya kuasnya, Kevin menyusun pencahayaannya. Sejak itu kami tahu kami tim yang baik." },
    { date: "2026", title: "Sebuah Kanvas Kosong", body: "Di studio kecil kami, Kevin menyerahkan kanvas berisi satu kalimat bertinta emas. Nadia menjawabnya dengan satu goresan: iya." },
  ],
  events: [
    { name: "Pengucapan Janji", date: "2027-08-14T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Galeri Tujuh, Ruang Putih Lt. 3", address: "Jl. Senopati No. 77, Selong, Kebayoran Baru, Jakarta Selatan" },
    { name: "Resepsi Senja", date: "2027-08-14T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Galeri Tujuh Rooftop", address: "Jl. Senopati No. 77, Selong, Kebayoran Baru, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r56.webp", "/themes/img/a123.webp", "/themes/img/r31.webp", "/themes/img/r2.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0814 27", account_name: "Nadia Paramitha Wijaya" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "OVO", ewallet_number: "0813 1408 2027", account_name: "Kevin Adrian Santoso" },
  ],
  guestName: "Bapak Yohanes Sutanto & Partner",
  guestTable: "Meja 08",
  extras: {
    rundown: { items: [
      { time: "16.00", title: "Tamu tiba, minuman selamat datang" },
      { time: "16.30", title: "Pengucapan janji di Ruang Putih" },
      { time: "18.30", title: "Resepsi dan makan malam di rooftop" },
      { time: "20.30", title: "Live painting & dansa pertama" },
    ] },
    dressCode: { note: "Hitam-putih formal. Sentuhan emas kecil sangat dipersilakan.", colors: ["#141414", "#fdfcf9", "#c9a24a"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Hendra Wijaya", "Keluarga Robert Santoso"] },
    faq: { items: [
      { q: "Apakah ada area parkir?", a: "Parkir tersedia di basemen gedung (akses dari Jl. Senopati). Valet tersedia mulai pukul 15.30." },
      { q: "Bolehkah membawa anak?", a: "Tentu. Kami menyiapkan meja menggambar dengan kuas air untuk tamu cilik." },
    ] },
  },
});
