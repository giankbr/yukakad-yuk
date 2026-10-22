import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Clara", groom: "Mikael",
    brideFull: "Clara Anindita Wibisono, S.Sn.", groomFull: "Mikael Sebastian Hutomo, S.Ars.",
    brideParents: "Putri kedua dari\nBapak Fransiskus Wibisono & Ibu Maria Lestari", groomParents: "Putra sulung dari\nBapak Yohanes Hutomo & Ibu Theresia Kurniasih",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Kami bertemu di depan kanvas yang sama, dan memutuskan untuk melukis sisa hidup bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T10:00:00+07:00",
  place: "Taman Kanvas Lembang",
  address: "Jl. Raya Lembang No. 168, Gudangkahuripan, Lembang, Bandung Barat",
  stories: [
    { date: "Juli 2021", title: "Kelas Melukis di Alam Terbuka", body: "Clara mengajar kelas lukis plein air di kebun teh Lembang. Mikael datang membawa kuas yang masih terbungkus plastik." },
    { date: "2023", title: "Pameran Kecil Berdua", body: "Dua puluh lukisan taman, satu galeri sewaan di Braga, dan seribu cangkir kopi untuk para tamu." },
    { date: "Desember 2026", title: "Lamaran di Tepi Kolam Teratai", body: "Mikael menyembunyikan cincin di balik palet cat. Clara baru melihatnya setelah lukisannya selesai." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-05-22T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gereja Santo Laurentius", address: "Jl. Sukajadi No. 223, Sukarasa, Sukasari, Kota Bandung" },
    { name: "Resepsi Taman", date: "2027-05-22T16:00:00+07:00", time: "16.00 – 20.00 WIB", venue: "Taman Kanvas Lembang", address: "Jl. Raya Lembang No. 168, Gudangkahuripan, Lembang, Bandung Barat" },
  ],
  gallery: ["/themes/img/r75.webp", "/themes/img/r13.webp", "/themes/img/r8.webp", "/themes/img/r16.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 2215 88", account_name: "Clara Anindita Wibisono" },
    { id: "demo-mandiri", type: "bank", bank_name: "Bank Mandiri", account_number: "130 00 1782 4419", account_name: "Mikael Sebastian Hutomo" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Timur No. 41, Cibeunying Kaler, Kota Bandung 40191" },
  ],
  guestName: "Ibu Veronika Sari & Keluarga",
  guestTable: "Meja Teratai 3",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati; ia tidak cemburu. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu.", source: "1 Korintus 13:4, 7" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu & musik gesek", note: "Jalan setapak mawar" },
      { time: "16.45", title: "Masuknya kedua mempelai" },
      { time: "17.15", title: "Lukis bersama di tepi kolam", note: "Satu kanvas besar untuk semua tamu" },
      { time: "18.00", title: "Santap malam di taman" },
    ] },
    dressCode: { note: "Warna-warna taman impresionis: hijau zaitun, merah muda mawar, biru kolam, dan krem kanvas. Sepatu nyaman untuk rumput.", colors: ["#6f8a48", "#e88aa0", "#7d9fb4", "#f4ecdc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Fransiskus Wibisono", "Kel. Besar Bpk. Yohanes Hutomo", "Komunitas Lukis Plein Air Bandung"] },
    travel: { note: "Lembang sejuk di sore hari. Berikut pilihan menginap dan parkir di sekitar taman.", items: [
      { name: "Parkir & shuttle", detail: "Parkir di lapangan Gudangkahuripan, shuttle tiap 15 menit" },
      { name: "Penginapan terdekat", detail: "± 1 km dari taman, kode tamu CLARAMIKAEL" },
    ] },
  },
});
