import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Dr. Rania Pramudita", groom: "Fikri Hidayat",
    brideFull: "Dr. Rania Pramudita, M.Sc.", groomFull: "Fikri Hidayat, S.Si., M.T.",
    brideParents: "Peneliti utama Laboratorium Material Berkelanjutan,\nFakultas Sains & Teknologi Universitas Cendekia Nusantara.",
    groomParents: "Dosen Kimia Material dan pengurus\nHimpunan Peneliti Material Muda Indonesia.",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Material Hijau untuk Kota Berkelanjutan: dari Laboratorium ke Industri",
  },
  eventLabel: "Seminar Nasional",
  date: "2027-04-24T08:00:00+07:00",
  place: "Auditorium Gedung Sains Terpadu",
  address: "Kampus Universitas Cendekia Nusantara, Jl. Lingkar Kampus No. 1, Depok, Sleman, Yogyakarta",
  story: { title: "Latar & Agenda", body: "" },
  stories: [
    { date: "Latar Belakang", title: "Mengapa material hijau?", body: "Sektor konstruksi menyumbang hampir 40 persen emisi karbon global. Seminar ini mempertemukan riset bahan bangunan rendah emisi dengan kebutuhan nyata industri dan pemerintah daerah." },
    { date: "Sesi 1 · 08.30", title: "Kuliah Utama", body: "Beton geopolimer dari abu terbang dan limbah sawit: hasil uji lapangan tiga tahun di Yogyakarta dan Riau." },
    { date: "Sesi 2 · 10.15", title: "Diskusi Panel", body: "Akademisi, pelaku industri, dan perencana kota membahas jalan dari prototipe laboratorium menuju standar nasional." },
    { date: "Sesi 3 · 13.00", title: "Presentasi Poster", body: "Dua puluh empat poster hasil riset mahasiswa pascasarjana, dinilai oleh dewan juri dari tiga universitas." },
  ],
  events: [
    { name: "Registrasi Ulang & Pembukaan", date: "2027-04-24T07:30:00+07:00", time: "07.30 – 08.30 WIB", venue: "Lobi Gedung Sains Terpadu", address: "Kampus Universitas Cendekia Nusantara, Jl. Lingkar Kampus No. 1, Depok, Sleman, Yogyakarta" },
    { name: "Seminar & Diskusi Panel", date: "2027-04-24T08:30:00+07:00", time: "08.30 – 15.00 WIB", venue: "Auditorium Gedung Sains Terpadu", address: "Kampus Universitas Cendekia Nusantara, Jl. Lingkar Kampus No. 1, Depok, Sleman, Yogyakarta" },
  ],
  gallery: ["/themes/img/r59.webp", "/themes/img/r71.webp", "/themes/img/r69.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "1290 4477 21", account_name: "Panitia Seminar Material Hijau" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 6610 2027", account_name: "Bendahara Panitia" },
  ],
  guestName: "Sdr. Arif Wicaksana",
  guestTable: "Kursi B-14",
  extras: {
    quote: { text: "Sains adalah cara berpikir, jauh lebih dari sekadar kumpulan pengetahuan.", source: "Carl Sagan" },
    rundown: { items: [
      { time: "07.30", title: "Registrasi ulang & kopi pagi" },
      { time: "08.30", title: "Kuliah utama", note: "Dr. Rania Pramudita, M.Sc." },
      { time: "10.15", title: "Diskusi panel & tanya jawab", note: "Moderator: Fikri Hidayat, S.Si., M.T." },
      { time: "12.00", title: "Istirahat & makan siang" },
      { time: "13.00", title: "Presentasi poster mahasiswa" },
      { time: "14.30", title: "Pengumuman poster terbaik & penutupan" },
    ] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-04-24T08:30:00+07:00", note: "Peserta daring dapat mengikuti kuliah utama dan diskusi panel melalui siaran langsung." },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Apakah peserta mendapat sertifikat?", a: "Ya. E-sertifikat dikirim ke surel peserta paling lambat tiga hari setelah acara." },
      { q: "Bisakah mengikuti secara daring?", a: "Bisa. Pilih \"Ikut daring\" saat konfirmasi, tautan siaran akan dikirim sehari sebelumnya." },
      { q: "Di mana parkir kendaraan?", a: "Parkir tersedia di gedung parkir timur kampus, sekitar tiga menit berjalan kaki." },
    ] },
  },
});
