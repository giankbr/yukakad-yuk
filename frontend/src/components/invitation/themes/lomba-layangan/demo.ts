import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Panitia Festival Angin Timur", groom: "Komunitas Layang Pesisir",
    brideFull: "Panitia Festival Layang-Layang Angin Timur", groomFull: "Komunitas Layang Pesisir Karangsari",
    brideParents: "Pemuda Desa Karangsari yang mengurus lapangan, juri, pengeras suara, konsumsi, dan hadiah. Ketua panitia: Mas Yoga Pratama.",
    groomParents: "Para perajin dan penerbang layangan yang berlatih tiap sore di pantai. Menyiapkan kelas membuat layangan dan tim juri.",
    note: "Dua hari angin laut, ratusan layangan, dan satu langit yang kita warnai bersama.",
  },
  eventLabel: "Festival Layang-Layang Angin Timur",
  date: "2027-08-07T07:00:00+07:00",
  place: "Pantai Pasir Panjang Karangsari",
  address: "Pantai Pasir Panjang, Desa Karangsari, Kec. Pesisir Kidul",
  story: { title: "Jadwal festival", body: "" },
  stories: [
    { date: "Sabtu · 07.00", title: "Daftar ulang & uji terbang", body: "Peserta mengambil nomor dan pita warna. Satu jam bebas untuk mencoba arah angin." },
    { date: "Sabtu · 09.00", title: "Lomba Layangan Tradisional", body: "Kategori wajik, ikan, dan kupu-kupu dari bambu dan kertas. Dinilai dari keindahan, kestabilan, dan ketinggian." },
    { date: "Sabtu · 14.00", title: "Kelas membuat layangan", body: "Untuk pemula dan keluarga. Bahan disediakan panitia, hasilnya boleh langsung diterbangkan." },
    { date: "Minggu · 08.00", title: "Lomba Layangan Kreasi", body: "Layangan modern, kotak, delta, dan rangkaian panjang. Tema tahun ini: laut dan isinya." },
    { date: "Minggu · 15.30", title: "Pengumuman juara", body: "Piala bergilir, medali, dan doorprize, lalu foto bersama dengan langit penuh layangan." },
  ],
  events: [
    { name: "Hari I · Layangan Tradisional", date: "2027-08-07T07:00:00+07:00", time: "07.00 – 17.00", venue: "Pantai Pasir Panjang Karangsari", address: "Pantai Pasir Panjang, Desa Karangsari, Kec. Pesisir Kidul (parkir di lapangan desa)" },
    { name: "Hari II · Layangan Kreasi & Final", date: "2027-08-08T07:00:00+07:00", time: "07.00 – 16.30", venue: "Pantai Pasir Panjang Karangsari", address: "Pantai Pasir Panjang, Desa Karangsari, Kec. Pesisir Kidul (parkir di lapangan desa)" },
  ],
  gallery: ["/themes/img/r103.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0563 0110 2287 504", account_name: "Bendahara Festival Angin Timur" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "DANA", ewallet_number: "0812 2650 7731", account_name: "Bendahara Festival Angin Timur" },
    { id: "demo-hadiah", type: "address", address: "Sekretariat Komunitas Layang Pesisir, Balai Desa Karangsari (bambu, kertas, benang, atau hadiah doorprize)" },
  ],
  guestName: "Kak Arif & Tim Garuda Biru",
  guestTable: "Peserta No. 27",
  extras: {
    rundown: { items: [
      { time: "06.30", title: "Lapangan dibuka", note: "Pasang tenda tim di zona yang ditentukan" },
      { time: "07.00", title: "Daftar ulang peserta", note: "Bawa layangan dan kartu peserta" },
      { time: "08.30", title: "Pembukaan oleh Kepala Desa" },
      { time: "09.00", title: "Babak penyisihan dimulai", note: "Ikuti aba-aba bendera juri" },
      { time: "12.00", title: "Istirahat & bazar kuliner pantai" },
    ] },
    guestPass: { note: "Tunjukkan kode ini di tenda panitia untuk mengambil nomor dada dan pita warna tim." },
    family: { title: "Didukung oleh", names: ["Karang Taruna Karangsari", "Warung Bu Darmi", "Toko Bambu Sinar Laut", "Kelompok Nelayan Pesisir"] },
    faq: { items: [
      { q: "Siapa yang boleh ikut lomba?", a: "Semua umur, perorangan atau tim (maksimal 4 orang). Anak di bawah 12 tahun didampingi orang tua." },
      { q: "Boleh pakai benang gelasan?", a: "Tidak. Demi keamanan penonton dan burung laut, hanya benang katun atau nilon polos yang diizinkan." },
      { q: "Penonton perlu daftar?", a: "Tidak perlu, gratis. Konfirmasi tetap membantu panitia menyiapkan tempat duduk dan air minum." },
    ] },
  },
});
