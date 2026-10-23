import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Elang", groom: "",
    brideFull: "Bima Elang Saputra",
    brideParents: "Putra pertama dari Bapak Reza Saputra & Ibu Nadia Kusuma",
    note: "Elang genap tujuh tahun! Bawa senter, jaket hangat, dan cerita seru. Kita berkemah di halaman, bakar marshmallow, dan hitung bintang bersama.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-08-14T16:00:00+07:00",
  place: "Halaman Rumah Keluarga Saputra",
  address: "Jl. Pandu Raya No. 18, Tegal Gundil, Kec. Bogor Utara, Kota Bogor",
  story: { title: "Cerita Elang", body: "" },
  stories: [
    { date: "2020", title: "Lahir di musim kemarau", body: "Elang lahir di malam yang cerah. Kata Ayah, bintangnya banyak sekali, seperti ikut menyambut." },
    { date: "2024", title: "Tenda pertama", body: "Tenda kecil dari Kakek dipasang di ruang tamu. Elang tidur di dalamnya tiga malam berturut-turut." },
    { date: "2027", title: "Tujuh tahun!", body: "Sekarang Elang sudah bisa memasang tenda sendiri dan ingin mengajak teman-temannya berkemah di halaman." },
  ],
  events: [
    { name: "Pesta Kemah Elang", date: "2027-08-14T16:00:00+07:00", time: "16.00 – 18.00 WIB", venue: "Halaman Rumah Keluarga Saputra", address: "Jl. Pandu Raya No. 18, Tegal Gundil, Kec. Bogor Utara, Kota Bogor" },
    { name: "Api Unggun & Cerita Malam", date: "2027-08-14T18:30:00+07:00", time: "18.30 – 20.00 WIB", venue: "Halaman belakang", address: "Jl. Pandu Raya No. 18, Tegal Gundil, Kec. Bogor Utara, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0341 0110 2207 509", account_name: "Nadia Kusuma" },
    { id: "demo-kado", type: "address", address: "Jl. Pandu Raya No. 18, Tegal Gundil, Kec. Bogor Utara, Kota Bogor 16152" },
  ],
  guestName: "Adik Kirana & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Bima Elang Saputra", nickname: "Elang", birthDate: "2020-08-12T21:10:00+07:00", parents: "Putra pertama dari Bapak Reza Saputra & Ibu Nadia Kusuma" },
    rundown: { items: [
      { time: "16.00", title: "Datang & pilih tenda", note: "Setiap anak dapat bandana dan senter kecil" },
      { time: "16.30", title: "Lomba pasang tenda mini" },
      { time: "17.15", title: "Jelajah halaman: cari jejak burung hantu" },
      { time: "18.30", title: "Api unggun, marshmallow & tiup lilin" },
    ] },
    dressCode: { note: "Pakaian nyaman ala anak kemah: kaus, celana panjang, dan jaket. Warna hutan dan oranye tenda.", colors: ["#e8743b", "#3e6b3a", "#ffc845", "#1d2a44"] },
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Saputra", "Opa & Oma Kusuma", "Tante Dinda"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Elang impikan.", items: [
      { id: "w1", name: "Teropong anak", price: "± Rp150.000" },
      { id: "w2", name: "Buku cerita rasi bintang", price: "± Rp95.000", claimed_by: "Tante Dinda" },
      { id: "w3", name: "Lampu tenda bentuk bulan", price: "± Rp80.000" },
    ] },
    faq: { items: [
      { q: "Apakah anak-anak menginap?", a: "Tidak, pesta selesai pukul 20.00. Tendanya untuk bermain dan bercerita." },
      { q: "Bagaimana jika hujan?", a: "Tenda dipindah ke garasi yang sudah kami hias. Api unggun diganti lampu hangat dan s'mores di dalam." },
    ] },
  },
});
