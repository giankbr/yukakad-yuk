import { makeDemo } from "../demo-base";

const ART = "/themes/art/pameran-seni";

export const demo = makeDemo({
  couple: {
    bride: "Laras Wening", groom: "Yudhistira Anom",
    brideFull: "Laras Wening Prameswari", groomFull: "Yudhistira Anom Prakoso, M.Sn.",
    brideParents: "Perupa kelahiran Pacitan, 1991. Lulusan Seni Murni ISI Yogyakarta; sepuluh tahun terakhir melukis garis pantai selatan Jawa.",
    groomParents: "Kurator independen dan pengajar sejarah seni rupa, tinggal dan bekerja di Yogyakarta.",
    note: "Dua puluh empat lukisan tentang garis yang ditinggalkan air di pasir: jejak yang selalu hilang, dan selalu kembali.",
  },
  eventLabel: "Pembukaan Pameran",
  date: "2027-08-14T19:00:00+07:00",
  place: "Galeri Lorong Teduh",
  address: "Jl. Suryodiningratan No. 9, Mantrijeron, Yogyakarta",
  story: { title: "Garis Pasang Surut", body: "" },
  stories: [
    { date: "Pasang", title: "Air yang Datang", body: "Seri pertama dilukis langsung di bibir pantai Klayar saat air naik: bidang-bidang warna yang ditekan oleh garis cakrawala." },
    { date: "Surut", title: "Garis yang Tertinggal", body: "Ketika air turun, pasir menyimpan garis-garis tipis. Laras menyalinnya dengan kuas kering, berulang, seperti mencatat napas." },
    { date: "Karang", title: "Yang Tetap Tinggal", body: "Bagian ketiga menumpuk bentuk-bentuk karang: benda yang bertahan di antara pasang dan surut, seperti ingatan." },
  ],
  events: [
    { name: "Pembukaan Pameran", date: "2027-08-14T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Galeri Lorong Teduh", address: "Jl. Suryodiningratan No. 9, Mantrijeron, Yogyakarta" },
    { name: "Diskusi Seniman & Kurator", date: "2027-08-15T15:00:00+07:00", time: "15.00 – 17.00 WIB", venue: "Ruang Baca Galeri Lorong Teduh", address: "Jl. Suryodiningratan No. 9, Mantrijeron, Yogyakarta" },
    { name: "Masa Pameran", date: "2027-08-15T10:00:00+07:00", time: "15 Agustus – 12 September 2027 · Selasa – Minggu, 10.00 – 19.00 WIB", venue: "Galeri Lorong Teduh", address: "Jl. Suryodiningratan No. 9, Mantrijeron, Yogyakarta" },
  ],
  gallery: [`${ART}/karya-1.webp`, `${ART}/karya-2.webp`, `${ART}/karya-3.webp`],
  gifts: [
    { id: "demo-katalog", type: "bank", bank_name: "BNI", account_number: "0721 3390 58", account_name: "Galeri Lorong Teduh (Katalog)" },
  ],
  guestName: "Ibu Ratna Sari Dewanti",
  guestTable: "Undangan Pembukaan",
  extras: {
    quote: { text: "Laut tidak pernah menggambar garis yang sama dua kali. Saya hanya mencoba mengingatnya sebelum air datang lagi.", source: "Laras Wening, catatan studio 2026" },
    rundown: { items: [
      { time: "19.00", title: "Registrasi & sambutan" },
      { time: "19.20", title: "Pengantar kuratorial", note: "Yudhistira Anom" },
      { time: "19.40", title: "Pembukaan resmi & tur karya", note: "Dipandu langsung oleh seniman" },
      { time: "20.30", title: "Ramah tamah & musik ambient" },
    ] },
    faq: { items: [
      { q: "Apakah pembukaan terbuka untuk umum?", a: "Pembukaan khusus undangan. Mulai 15 Agustus pameran terbuka untuk umum tanpa biaya masuk." },
      { q: "Bolehkah memotret karya?", a: "Boleh, tanpa lampu kilat. Mohon tidak menyentuh karya dan menjaga jarak satu langkah dari dinding." },
      { q: "Apakah karya dijual?", a: "Sebagian karya tersedia untuk koleksi. Daftar harga dapat diminta di meja resepsionis." },
    ] },
    guestPass: {},
  },
});
