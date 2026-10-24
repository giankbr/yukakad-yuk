import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Panitia Makrab 2027", groom: "",
    brideFull: "Himpunan Mahasiswa Arsitektur Lanskap (HIMALA)",
    brideParents: "Fakultas Desain & Lingkungan Binaan\nUniversitas Cendekia Raya, Malang",
    note: "Satu angkatan baru, satu api unggun, dan satu malam untuk saling kenal sebelum tugas studio menumpuk.",
  },
  eventLabel: "Malam Keakraban",
  date: "2027-09-18T13:00:00+07:00",
  place: "Villa Kabut Pinus",
  address: "Jl. Raya Cangar Km 4, Sumberbrantas, Bumiaji, Kota Batu",
  story: { title: "Susunan Acara", body: "" },
  stories: [
    { date: "Sabtu, 13.00", title: "Kumpul & berangkat", body: "Absen di lobi Gedung C, bagi kelompok, lalu naik bus ke Batu. Jangan lupa jaket." },
    { date: "Sabtu, 16.00", title: "Tiba & bagi kamar", body: "Taruh tas, ngopi sore di teras villa, foto angkatan pertama dengan latar gunung." },
    { date: "Sabtu, 19.00", title: "Api unggun & perkenalan", body: "Satu per satu kenalan di depan api: nama, asal, dan satu fakta yang nggak ada di KTM." },
    { date: "Sabtu, 21.00", title: "Pentas kelompok & gitar", body: "Tiap kelompok tampil lima menit. Bebas: lagu, drama, atau stand-up. Lalu nyanyi bareng sampai suara habis." },
    { date: "Minggu, 06.00", title: "Senam pagi & games", body: "Estafet sarung, tebak gambar, dan tarik tambang kakak tingkat lawan maba. Pulang setelah makan siang." },
  ],
  events: [
    { name: "Kumpul & Keberangkatan", date: "2027-09-18T13:00:00+07:00", time: "13.00 WIB", venue: "Lobi Gedung C, Kampus Cendekia Raya", address: "Jl. Veteran Barat No. 21, Ketawanggede, Lowokwaru, Kota Malang" },
    { name: "Makrab di Villa", date: "2027-09-18T16:00:00+07:00", time: "Sabtu 16.00 – Minggu 13.00 WIB", venue: "Villa Kabut Pinus", address: "Jl. Raya Cangar Km 4, Sumberbrantas, Bumiaji, Kota Batu" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-iuran", type: "ewallet", ewallet_provider: "DANA", ewallet_number: "0857 3011 2027", account_name: "Salsa (Bendahara Makrab)" },
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "1902 7700 18", account_name: "Salsabila Putri" },
  ],
  guestName: "Rizky Ananda",
  guestTable: "Kelompok Cemara",
  extras: {
    dressCode: { note: "Kaos angkatan (dibagikan saat registrasi), jaket tebal, celana panjang, sepatu yang nyaman. Malam di Cangar bisa 14°C.", colors: ["#2f4fa2", "#ff4fa8", "#ffd31a", "#0a9a8e"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Wajib ikut?", a: "Nggak wajib, tapi sangat disarankan. Ini satu-satunya malam satu angkatan bisa kumpul lengkap sebelum semester sibuk." },
      { q: "Perlu bawa apa?", a: "Jaket, sleeping bag atau selimut, obat pribadi, botol minum, dan alat musik kalau punya. Makan disediakan panitia." },
      { q: "Iurannya berapa?", a: "Rp175.000 sudah termasuk bus pulang-pergi, villa, tiga kali makan, dan kaos angkatan." },
    ] },
  },
});
