import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Prof. Hendra Wiratama", groom: "Dr. Laksmi Pramesti",
    brideFull: "Prof. Dr. Ir. Hendra Wiratama, M.Sc.", groomFull: "Dr. Laksmi Pramesti, S.E., M.M.",
    brideParents: "Rektor Universitas Nusa Bahari\nperiode 2024 – 2028",
    groomParents: "Ketua Panitia\nDies Natalis ke-50",
    note: "Lima puluh tahun menimba ilmu dari laut, lima puluh tahun mengabdi untuk negeri kepulauan.",
  },
  eventLabel: "Dies Natalis ke-50 Universitas Nusa Bahari",
  date: "2027-10-16T08:00:00+07:00",
  place: "Auditorium Samudra",
  address: "Kampus Universitas Nusa Bahari, Jl. Pantai Kenjeran No. 50, Bulak, Surabaya",
  story: { title: "Jejak sejarah", body: "" },
  stories: [
    { date: "1977", title: "Akademi Pelayaran Kecil", body: "Berdiri sebagai akademi dengan 64 mahasiswa, dua ruang kuliah pinjaman, dan satu kapal latih kayu di pelabuhan rakyat." },
    { date: "1989", title: "Menjadi Universitas", body: "Resmi berstatus universitas dengan empat fakultas: Teknik Kelautan, Perikanan, Ekonomi Maritim, dan Keguruan." },
    { date: "2008", title: "Gedung Rektorat & Menara Jam", body: "Gedung rektorat bermenara jam diresmikan dan menjadi wajah kampus di tepi Pantai Kenjeran hingga hari ini." },
    { date: "2027", title: "Setengah Abad", body: "Lebih dari 61.000 alumni berkarya di pelabuhan, laboratorium, sekolah, dan pemerintahan di seluruh Nusantara." },
  ],
  events: [
    { name: "Rapat Senat Terbuka", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 11.30 WIB", venue: "Auditorium Samudra", address: "Kampus Universitas Nusa Bahari, Jl. Pantai Kenjeran No. 50, Bulak, Surabaya" },
    { name: "Malam Temu Alumni", date: "2027-10-16T18:30:00+07:00", time: "18.30 – 22.00 WIB", venue: "Lapangan Menara Jam", address: "Kampus Universitas Nusa Bahari, Jl. Pantai Kenjeran No. 50, Bulak, Surabaya" },
  ],
  gallery: ["/themes/img/r59.webp", "/themes/img/r94.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0950 5019 77", account_name: "Dana Abadi Universitas Nusa Bahari" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "142 00 1977 5050", account_name: "Ikatan Alumni Nusa Bahari (Beasiswa)" },
  ],
  guestName: "Bapak Ir. Daniel Siregar (Alumni Teknik Kelautan 1989)",
  guestTable: "Tribun Alumni B",
  extras: {
    quote: { text: "Ilmu yang berlayar jauh selalu tahu jalan pulang ke pelabuhan tempat ia dibesarkan.", source: "Moto Dies Natalis ke-50" },
    rundown: { items: [
      { time: "08.00", title: "Prosesi senat", note: "Guru besar & anggota senat memasuki auditorium" },
      { time: "08.45", title: "Laporan tahunan rektor" },
      { time: "09.30", title: "Orasi ilmiah", note: "\"Laut sebagai Masa Depan Pangan Indonesia\"" },
      { time: "11.00", title: "Penganugerahan alumni berprestasi" },
      { time: "18.30", title: "Malam temu alumni", note: "Bazar angkatan & pentas paduan suara" },
    ] },
    dressCode: { note: "Rapat senat: busana resmi, jas atau batik lengan panjang. Malam temu alumni: batik atau kaus angkatan.", colors: ["#173b41", "#c9a24c", "#f4ecd8", "#b03a2e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T08:00:00+07:00", note: "Rapat senat terbuka disiarkan langsung." },
    guestPass: { note: "Tunjukkan kode ini di meja registrasi auditorium." },
    rsvpDietary: { label: "Butuh kursi roda atau akses khusus? (opsional)" },
    faq: { items: [
      { q: "Apakah alumni boleh membawa keluarga?", a: "Boleh untuk Malam Temu Alumni. Rapat senat terbuka terbatas bagi undangan karena kapasitas auditorium." },
      { q: "Di mana tempat parkir?", a: "Parkir tersedia di gedung parkir utara. Shuttle kampus beroperasi setiap 10 menit." },
    ] },
  },
});
