import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Bayu",
    brideFull: "Sekar Ayu Kinanti", groomFull: "Bayu Satria Nugraha",
    brideParents: "Putri dari Bapak Wahyu Prasetyo\n& Ibu Rini Anggraeni", groomParents: "Putra dari Bapak Dadang Suherman\n& Ibu Euis Komalasari",
    note: "Kami sudah ratusan kilometer mengayuh berdua. Mulai hari ini, kami ingin mengayuh sisa jalan hidup dengan satu sepeda.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Rumah Kebun Sukawana",
  address: "Jl. Sukawana No. 21, Karyawangi, Parongpong, Bandung Barat",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Minggu pagi, 2022", title: "Gowes Bareng Komunitas", body: "Rantai sepeda Sekar putus di tanjakan Dago. Bayu, yang tertinggal paling belakang, ternyata membawa rantai cadangan." },
    { date: "2024", title: "Tandem Pertama", body: "Kami menyewa sepeda tandem di Lembang dan tertawa sepanjang jalan karena tidak pernah kompak mengayuh." },
    { date: "2026", title: "Keranjang Bunga", body: "Di jalan desa yang sama, Bayu menaruh cincin di antara bunga-bunga di keranjang sepeda. Sekar menjawab sambil terus mengayuh: iya." },
    { date: "Juli 2027", title: "Satu Sepeda, Dua Hati", body: "Kami merayakannya di kebun yang dikelilingi ladang, bersama keluarga dan sahabat seperjalanan." },
  ],
  events: [
    { name: "Ikrar Janji Pernikahan", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Pendopo Kebun, Rumah Kebun Sukawana", address: "Jl. Sukawana No. 21, Karyawangi, Parongpong, Bandung Barat" },
    { name: "Resepsi Taman", date: "2027-07-10T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Taman Lavender, Rumah Kebun Sukawana", address: "Jl. Sukawana No. 21, Karyawangi, Parongpong, Bandung Barat" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r1.webp", "/themes/img/r2.webp", "/themes/img/a123.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0172 0100 7277", account_name: "Sekar Ayu Kinanti" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "DANA", ewallet_number: "0812 2207 1027", account_name: "Bayu Satria Nugraha" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Barat No. 9, Cibeunying Kaler, Kota Bandung 40191" },
  ],
  guestName: "Kang Rizal & Teh Wulan",
  guestTable: "Meja Lavender 4",
  extras: {
    rundown: { items: [
      { time: "08.30", title: "Tamu datang, teh hangat dan kue serabi" },
      { time: "09.00", title: "Ikrar janji di pendopo kebun" },
      { time: "11.00", title: "Resepsi taman dan makan siang prasmanan" },
      { time: "13.00", title: "Foto bersama di jalan ladang dengan sepeda tandem" },
    ] },
    dressCode: { note: "Santai rapi ala piknik: warna pastel, kain linen, sepatu datar yang nyaman di rumput.", colors: ["#d4573b", "#e8b64a", "#8fc3d3", "#c3b0dc"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Wahyu Prasetyo", "Keluarga Dadang Suherman"] },
    faq: { items: [
      { q: "Bagaimana menuju lokasi?", a: "Dari Lembang ikuti arah Parongpong sekitar 20 menit. Jalan terakhir sempit, mobil kecil dan motor lebih nyaman." },
      { q: "Bolehkah datang bersepeda?", a: "Boleh sekali! Kami menyiapkan parkir sepeda dan air minum di gerbang kebun." },
    ] },
  },
});
