import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Dr. Anindya Prameswari", groom: "Bayu Aditama",
    brideFull: "Dr. Anindya Prameswari, M.Pd.", groomFull: "Bayu Aditama, S.Hum.",
    brideParents: "Pengurus Pusat PELITA\nMasa Bakti 2027 – 2030", groomParents: "Koordinator Rumah Baca Jawa Tengah\nPanitia Pelantikan 2027",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Menyalakan pelita di setiap kampung: satu rak buku, satu relawan, satu anak yang jatuh cinta pada membaca.",
  },
  eventLabel: "Pelantikan Pengurus Pusat PELITA",
  date: "2027-02-20T09:00:00+07:00",
  place: "Aula Graha Wiyata",
  address: "Jl. Pandanaran No. 88, Mugassari, Semarang Selatan, Kota Semarang",
  story: { title: "Perjalanan organisasi", body: "" },
  stories: [
    { date: "2015", title: "Lima Rak di Teras Rumah", body: "Perhimpunan Pecinta Literasi Nusantara (PELITA) bermula dari lima rak buku di teras rumah relawan di Ungaran." },
    { date: "2019", title: "Empat Puluh Rumah Baca", body: "Jaringan rumah baca tumbuh ke 40 titik di Jawa Tengah dengan lebih dari 300 relawan pendamping." },
    { date: "2026", title: "Musyawarah Nasional III", body: "Munas di Semarang memilih ketua umum baru dan menetapkan program kerja tiga tahun ke depan." },
    { date: "2027", title: "Agenda Masa Bakti Baru", body: "Perpustakaan keliling di 12 kabupaten, kelas menulis remaja, dan digitalisasi koleksi rumah baca." },
  ],
  events: [
    { name: "Pelantikan & Serah Terima Jabatan", date: "2027-02-20T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Aula Graha Wiyata", address: "Jl. Pandanaran No. 88, Mugassari, Semarang Selatan, Kota Semarang" },
    { name: "Rapat Kerja Perdana", date: "2027-02-20T13:30:00+07:00", time: "13.30 – 16.00 WIB", venue: "Ruang Sidang Lt. 2 Graha Wiyata", address: "Jl. Pandanaran No. 88, Mugassari, Semarang Selatan, Kota Semarang" },
  ],
  gallery: ["/themes/img/r94.webp"],
  gifts: [
    { id: "demo-papan", type: "address", address: "Aula Graha Wiyata, Jl. Pandanaran No. 88, Semarang (diterima H-1 pukul 15.00 – 20.00 WIB)" },
    { id: "demo-donasi", type: "bank", bank_name: "BRI", account_number: "0087 0100 2015 300", account_name: "Perhimpunan Pecinta Literasi Nusantara" },
  ],
  guestName: "Bapak Drs. Haryanto Wibowo (Dewan Pembina)",
  guestTable: "Kursi Undangan A-12",
  extras: {
    quote: { text: "Membaca adalah cara paling sederhana untuk menyalakan masa depan.", source: "Moto PELITA" },
    rundown: { items: [
      { time: "08.30", title: "Registrasi undangan", note: "Penyerahan kartu masuk di meja panitia" },
      { time: "09.00", title: "Pembukaan & menyanyikan lagu Indonesia Raya" },
      { time: "09.30", title: "Pembacaan SK & pengambilan sumpah pengurus" },
      { time: "10.15", title: "Serah terima jabatan & sambutan ketua umum" },
      { time: "11.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Pengurus: jas organisasi. Undangan: batik atau busana formal.", colors: ["#5c1324", "#1f5257", "#c9a24a", "#f7f1e3"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-02-20T09:00:00+07:00", note: "Prosesi pelantikan disiarkan langsung." },
    guestPass: { note: "Tunjukkan kode ini di meja registrasi." },
    rsvpDietary: { label: "Butuh akses kursi roda atau pendamping? (opsional)" },
    faq: { items: [
      { q: "Apakah undangan boleh diwakilkan?", a: "Boleh. Mohon konfirmasi nama perwakilan melalui form kehadiran." },
      { q: "Di mana tempat parkir?", a: "Parkir tersedia di halaman Graha Wiyata dan gedung parkir sebelah timur." },
    ] },
  },
});
