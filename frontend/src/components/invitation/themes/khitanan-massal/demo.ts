import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Yayasan Cahaya Ummah", groom: "DKM Masjid Al-Ikhlas",
    brideFull: "Yayasan Sosial Cahaya Ummah", groomFull: "Dewan Kemakmuran Masjid Al-Ikhlas Cibubur",
    brideParents: "Yayasan sosial yang sejak 2015 mendampingi keluarga prasejahtera di Cibubur dan sekitarnya melalui santunan, beasiswa, dan khitanan massal tahunan.",
    groomParents: "Pengurus dan jamaah masjid yang menyiapkan tempat, konsumsi, dan relawan pendamping anak selama acara berlangsung.",
    note: "Gratis untuk 100 anak laki-laki usia 5–12 tahun. Setiap peserta pulang membawa sarung, peci, bingkisan, dan uang saku.",
  },
  eventLabel: "Khitanan Massal",
  date: "2027-07-04T07:00:00+07:00",
  place: "Masjid Al-Ikhlas Cibubur",
  address: "Jl. Raya Lapangan Tembak No. 17, Cibubur, Ciracas, Jakarta Timur",
  story: { title: "Susunan program", body: "" },
  stories: [
    { date: "07.00", title: "Registrasi & Sarapan", body: "Orang tua membawa kartu peserta. Anak-anak mendapat nomor antrean, sarapan, dan kaus seragam." },
    { date: "08.00", title: "Pembukaan & Doa Bersama", body: "Sambutan ketua yayasan, tausiyah singkat tentang sunnah khitan, dan doa bersama para orang tua." },
    { date: "08.30", title: "Pelaksanaan Khitan", body: "Ditangani tim tenaga kesehatan berpengalaman di ruang yang bersih dan nyaman. Orang tua boleh mendampingi." },
    { date: "11.30", title: "Bingkisan & Santunan", body: "Setiap anak menerima sarung, peci, bingkisan, dan uang saku. Ditutup dengan penampilan marawis remaja masjid." },
  ],
  events: [
    { name: "Khitanan Massal", date: "2027-07-04T07:00:00+07:00", time: "07.00 – 12.00 WIB", venue: "Masjid Al-Ikhlas Cibubur", address: "Jl. Raya Lapangan Tembak No. 17, Cibubur, Ciracas, Jakarta Timur" },
    { name: "Kunjungan Kontrol", date: "2027-07-07T08:00:00+07:00", time: "08.00 – 11.00 WIB", venue: "Aula Yayasan Cahaya Ummah", address: "Jl. Kenari II No. 9, Cibubur, Ciracas, Jakarta Timur" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4560 88", account_name: "Yayasan Sosial Cahaya Ummah" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0813 1177 2045", account_name: "Bendahara Cahaya Ummah" },
    { id: "demo-barang", type: "address", address: "Sekretariat Cahaya Ummah, Jl. Kenari II No. 9, Cibubur, Jakarta Timur 13720 (sarung, peci, perlengkapan sekolah)" },
  ],
  guestName: "Bapak Hendra Gunawan",
  guestTable: "Peserta No. 27",
  extras: {
    quote: { text: "Lima hal termasuk fitrah: khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan memendekkan kumis.", source: "HR. Bukhari dan Muslim" },
    rundown: { items: [
      { time: "07.00", title: "Registrasi peserta", note: "Bawa kartu peserta dan fotokopi KK" },
      { time: "08.00", title: "Pembukaan & doa bersama" },
      { time: "08.30", title: "Pelaksanaan khitan sesuai nomor antrean" },
      { time: "11.30", title: "Pembagian bingkisan & santunan" },
    ] },
    dressCode: { note: "Anak-anak memakai kaus longgar dan sarung yang nyaman. Orang tua berbusana muslim yang sopan.", colors: ["#2f9e6b", "#f7c948", "#ffffff", "#ef6f5e"] },
    guestPass: { note: "Tunjukkan kode ini di meja registrasi untuk mengambil nomor antrean anak." },
    rsvpDietary: { label: "Nama dan usia anak (contoh: Raka, 7 tahun)" },
    faq: { items: [
      { q: "Siapa yang boleh mendaftar?", a: "Anak laki-laki usia 5–12 tahun, diutamakan dari keluarga prasejahtera dan anak yatim. Kuota 100 anak." },
      { q: "Apa yang perlu dibawa?", a: "Kartu peserta, fotokopi Kartu Keluarga, dan sarung. Anak sebaiknya sudah sarapan dan mandi." },
      { q: "Bagaimana jika berhalangan?", a: "Kabari panitia lewat form ini paling lambat tiga hari sebelum acara agar kuota bisa dialihkan." },
    ] },
  },
});
