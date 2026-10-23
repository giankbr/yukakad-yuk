import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinanti", groom: "Bagas",
    brideFull: "Kinanti Ayu Lestari", groomFull: "Bagas Satria Nugraha",
    brideParents: "Putri bungsu dari\nBapak Yusuf Hartanto & Ibu Melani Susanti", groomParents: "Putra kedua dari\nBapak Robertus Nugraha & Ibu Agnes Wulandari",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Bawa topi, bawa senyum. Selimut, roti lapis, dan limun dingin sudah kami siapkan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T11:00:00+07:00",
  place: "Padang Rumput Villa Kinara",
  address: "Jl. Kolonel Masturi No. 88, Cikahuripan, Lembang, Kabupaten Bandung Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Segelas Limun di Dago", body: "Bagas berjualan limun di Car Free Day Dago. Kinanti membeli satu gelas tiap Minggu, lalu lama-lama membeli dua." },
    { date: "2023", title: "Piknik Pertama", body: "Selimut kotak-kotak pinjaman Ibu, roti lapis yang agak gosong, dan sore panjang di Taman Hutan Raya Juanda." },
    { date: "2026", title: "Di Atas Selimut yang Sama", body: "Di antara stroberi dan bunga liar, Bagas mengeluarkan cincin dari keranjang rotan. Kinanti tertawa, lalu menangis, lalu bilang iya." },
  ],
  events: [
    { name: "Janji Nikah", date: "2027-05-15T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Gazebo Taman Villa Kinara", address: "Jl. Kolonel Masturi No. 88, Cikahuripan, Lembang, Kabupaten Bandung Barat" },
    { name: "Resepsi Piknik", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Padang Rumput Villa Kinara", address: "Jl. Kolonel Masturi No. 88, Cikahuripan, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/r79.webp", "/themes/img/r8.webp", "/themes/img/r9.webp", "/themes/img/a111.webp", "/themes/img/r14.webp", "/themes/img/r13.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0215 2705", account_name: "Kinanti Ayu Lestari" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0857 2015 0527", account_name: "Bagas Satria Nugraha" },
    { id: "demo-kado", type: "address", address: "Jl. Bukit Dago Utara No. 21, Coblong, Kota Bandung 40135" },
  ],
  guestName: "Mbak Sarah & Mas Dimas",
  guestTable: "Selimut 4",
  extras: {
    quote: { text: "Kebahagiaan itu sederhana: selimut di atas rumput, makanan yang dibagi, dan orang-orang tersayang yang duduk berdekatan.", source: "Kinanti & Bagas" },
    rundown: { items: [
      { time: "11.00", title: "Selamat datang & limun dingin", note: "Ambil selimut dan topi di meja depan" },
      { time: "11.30", title: "Kirab kecil kedua mempelai" },
      { time: "12.00", title: "Makan siang piknik", note: "Keranjang dibagikan per selimut" },
      { time: "13.30", title: "Permainan & foto bersama", note: "Lempar bola, balap karung, dan potret keluarga" },
    ] },
    dressCode: { note: "Gaya piknik santai: warna cerah, bahan katun, alas kaki datar. Rumputnya empuk!", colors: ["#d8443a", "#fff8ea", "#6f9a4a", "#f5cf3d"] },
    guestPass: {},
    rsvpDietary: { label: "Ada pantangan makanan? Kami siapkan keranjang khusus (opsional)" },
    family: { names: ["Kel. Besar Bpk. Yusuf Hartanto", "Kel. Besar Bpk. Robertus Nugraha"] },
    wishlist: { note: "Kehadiranmu sudah cukup. Kalau ingin memberi, ini yang kami impikan untuk rumah kecil kami.", items: [
      { id: "w1", name: "Keranjang piknik rotan", price: "± Rp450.000" },
      { id: "w2", name: "Set gelas & teko kaca", price: "± Rp300.000", claimed_by: "Mbak Sarah" },
      { id: "w3", name: "Tanaman hias untuk teras", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Bagaimana kalau hujan?", a: "Tenda transparan sudah disiapkan di sisi padang rumput. Piknik tetap jalan." },
      { q: "Boleh membawa anak?", a: "Boleh sekali! Ada area main dan keranjang camilan untuk anak-anak." },
    ] },
  },
});
