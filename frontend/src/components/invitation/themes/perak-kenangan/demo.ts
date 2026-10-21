import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ratna", groom: "Hendra",
    brideFull: "Ratna Kusumawardani", groomFull: "Hendra Wijayakusuma",
    brideParents: "Putri dari\nBapak (Alm.) Soedarmo & Ibu Sri Hartini", groomParents: "Putra dari\nBapak Sutopo Wijaya & Ibu (Almh.) Endang Lestari",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Dua puluh lima tahun yang lalu kami berjanji di hadapan keluarga. Hari ini kami ingin mensyukurinya bersama orang-orang yang menemani perjalanan itu.",
  },
  eventLabel: "Ulang Tahun Pernikahan ke-25",
  date: "2027-08-14T18:30:00+07:00",
  place: "Pendopo Kayu Manis",
  address: "Jl. Ijen No. 42, Oro-oro Dowo, Klojen, Kota Malang",
  stories: [
    { date: "1999", title: "Kenalan di Bus Kota", body: "Dua mahasiswa yang selalu naik bus jurusan Arjosari pukul tujuh pagi, sampai suatu hari Hendra memberanikan diri menyapa." },
    { date: "2002", title: "Akad & Resepsi Sederhana", body: "Menikah di rumah eyang di Kayutangan, dengan tenda biru dan nasi kotak buatan para tetangga." },
    { date: "2005", title: "Dimas Lahir", body: "Rumah kontrakan kecil kami mendadak terasa penuh. Lalu menyusul Laras (2008) dan Bintang (2013)." },
    { date: "2016", title: "Rumah Sendiri", body: "Setelah bertahun-tahun menabung, kami menanam pohon mangga di halaman rumah pertama kami sendiri." },
    { date: "2027", title: "Dua Puluh Lima Tahun", body: "Rambut mulai memutih, tetapi kami masih suka berjalan pagi bersama di Jalan Ijen." },
  ],
  events: [
    { name: "Syukuran & Makan Malam", date: "2027-08-14T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Pendopo Kayu Manis", address: "Jl. Ijen No. 42, Oro-oro Dowo, Klojen, Kota Malang" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/a34.webp", "/themes/img/a22.webp", "/themes/img/a50.webp", "/themes/img/a116.webp", "/themes/img/a111.webp"],
  gifts: [],
  guestName: "Om Bambang & Tante Wulan",
  guestTable: "Meja 7",
  extras: {
    quote: { text: "Cinta bukan tentang saling memandang, tetapi tentang bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Pameran foto kenangan di serambi" },
      { time: "19.00", title: "Doa syukur & pembaruan janji" },
      { time: "19.30", title: "Makan malam bersama" },
      { time: "20.30", title: "Persembahan anak-anak", note: "Dimas, Laras & Bintang" },
    ] },
    dressCode: { note: "Nuansa perak, putih gading, dan champagne.", colors: ["#c7ccd2", "#f3eee6", "#d9c3a0", "#8e95a0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Dimas, Laras & Bintang", "Keluarga Besar Soedarmo", "Keluarga Besar Sutopo Wijaya"] },
  },
});
