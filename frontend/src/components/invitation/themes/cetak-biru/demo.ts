import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Arga",
    brideFull: "Nadia Paramitha Kusuma, S.Ars.", groomFull: "Arga Wiratama Putra, S.T.",
    brideParents: "Putri pertama dari\nBapak Ir. Hendra Kusuma & Ibu Ratna Dewi", groomParents: "Putra kedua dari\nBapak Bambang Wiratama & Ibu Sri Lestari",
    bridePhoto: "/themes/img/a79.webp", groomPhoto: "/themes/img/a81.webp",
    note: "Kami sudah menggambar rumahnya berkali-kali. Kini saatnya membangun yang paling penting: rumah tangga.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T10:00:00+07:00",
  place: "Rumah Kaca Dago",
  address: "Jl. Dago Pakar Timur No. 21, Mekarsaluyu, Cimenyan, Bandung",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2016", title: "Studio Tingkat Akhir", body: "Satu meja gambar, dua maket yang tak kunjung selesai, dan kopi sachet pukul tiga pagi menjelang asistensi." },
    { date: "2021", title: "Proyek Pertama", body: "Nadia merancang, Arga menghitung struktur. Rumah kecil untuk orang tua Nadia di Ciumbuleuit jadi karya bersama pertama kami." },
    { date: "2027", title: "Fondasi Baru", body: "Gambar kerjanya sudah final. Dengan restu keluarga, kami mulai membangun rumah tangga." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-10-09T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Rumah Kaca Dago", address: "Jl. Dago Pakar Timur No. 21, Mekarsaluyu, Cimenyan, Bandung" },
    { name: "Resepsi Taman", date: "2027-10-09T16:00:00+07:00", time: "16.00 – 20.00 WIB", venue: "Taman Rumah Kaca Dago", address: "Jl. Dago Pakar Timur No. 21, Mekarsaluyu, Cimenyan, Bandung" },
  ],
  gallery: ["/themes/img/a80.webp", "/themes/img/a82.webp", "/themes/img/r43.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "7310 5521 08", account_name: "Nadia Paramitha Kusuma" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "130 00 1774 2290", account_name: "Arga Wiratama Putra" },
    { id: "demo-kado", type: "address", address: "Jl. Ciumbuleuit No. 142B, Hegarmanah, Cidadap, Bandung 40131" },
  ],
  guestName: "Sdr. Rizky Pratama & Partner",
  guestTable: "Meja A-04",
  extras: {
    quote: { text: "Rumah bukan soal luas bangunan, melainkan siapa yang menunggu di balik pintunya.", source: "Catatan di pojok gambar kerja kami" },
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Keluarga & sahabat terdekat" },
      { time: "16.00", title: "Resepsi taman dibuka" },
      { time: "17.30", title: "Tur maket rumah impian", note: "Maket 1:50 dipamerkan di teras" },
      { time: "18.30", title: "Makan malam & musik akustik" },
    ] },
    dressCode: { note: "Smart casual. Biru, putih, dan abu-abu dipersilakan. Sepatu datar disarankan: resepsi di taman berumput.", colors: ["#1f5fa6", "#f3f9ff", "#8fa3b8", "#2a3240"] },
    guestPass: {},
    rsvpDietary: {},
    wishlist: { items: [
      { id: "w1", name: "Set pisau dapur", price: "± Rp900.000" },
      { id: "w2", name: "Lampu baca meja gambar", price: "± Rp650.000", claimed_by: "Studio 7" },
      { id: "w3", name: "Tanaman untuk taman depan", price: "Bebas" },
    ] },
    family: { names: ["Kel. Besar Ir. Hendra Kusuma", "Kel. Besar Bambang Wiratama"] },
  },
});
