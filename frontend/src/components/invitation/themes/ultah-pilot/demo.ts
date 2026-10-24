import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gibran", groom: "",
    brideFull: "Danendra Gibran Mahesa",
    brideParents: "Putra pertama dari Bapak Rizky Mahesa & Ibu Anindya Paramitha",
    note: "Kapten Gibran siap lepas landas di umur empat! Kencangkan sabuk pengaman, kita terbang bersama ke pesta.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-08-14T10:00:00+07:00",
  place: "Rumah Pohon Playground",
  address: "Jl. Raya Darmo Permai III No. 7, Pradahkalikendal, Dukuh Pakis, Surabaya",
  stories: [
    { date: "2023", title: "Mendarat dengan selamat", body: "Gibran lahir di pagi yang cerah bulan Agustus, langsung menguasai kabin rumah dengan suara nyaringnya." },
    { date: "2025", title: "Pesawat pertama", body: "Hadiah ulang tahun ke-2 berupa pesawat baling-baling kayu yang sampai sekarang ikut tidur setiap malam." },
    { date: "2026", title: "Melihat pesawat sungguhan", body: "Kunjungan ke bandara membuat Gibran melambaikan tangan ke setiap pesawat yang lepas landas." },
    { date: "2027", title: "Kapten empat tahun", body: "Sekarang sudah hafal bunyi baling-baling dan selalu siap jadi pilot di setiap permainan." },
  ],
  events: [
    { name: "Pesta Pilot Cilik", date: "2027-08-14T10:00:00+07:00", time: "10.00 – 12.30 WIB", venue: "Rumah Pohon Playground", address: "Jl. Raya Darmo Permai III No. 7, Pradahkalikendal, Dukuh Pakis, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "142 00 1987 6543", account_name: "Anindya Paramitha" },
    { id: "demo-kado", type: "address", address: "Jl. Bukit Darmo Golf Blok R-12, Dukuh Pakis, Surabaya 60226" },
  ],
  guestName: "Dek Alea & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Danendra Gibran Mahesa", nickname: "Gibran", birthDate: "2023-08-14T07:15:00+07:00", parents: "Putra pertama dari Bapak Rizky Mahesa & Ibu Anindya Paramitha" },
    quote: { text: "Terbanglah setinggi mimpimu, Nak, dan selalu ingat jalan pulang ke rumah.", source: "Ayah & Bunda" },
    rundown: { items: [
      { time: "10.00", title: "Check-in & pembagian topi pilot", note: "Semua penumpang dapat lencana sayap" },
      { time: "10.30", title: "Lomba pesawat kertas" },
      { time: "11.15", title: "Tiup lilin & potong kue", note: "Nyanyi bersama" },
      { time: "12.00", title: "Pembagian goodie bag" },
    ] },
    dressCode: { note: "Baju pilot, pramugari, atau kaos warna langit. Merah, kuning, biru, dan putih.", colors: ["#e8473c", "#ffc93c", "#22427a", "#8fd0f2"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Mahesa", "Opa & Oma Paramitha"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Gibran.", items: [
      { id: "w1", name: "Pesawat mainan baling-baling", price: "± Rp180.000" },
      { id: "w2", name: "Buku cerita tentang pesawat", price: "± Rp85.000", claimed_by: "Tante Sasa" },
      { id: "w3", name: "Set topi & jaket pilot", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Perlu membawa kostum?", a: "Tidak wajib. Topi pilot dan lencana sayap disediakan untuk semua anak." },
      { q: "Apakah ada area untuk orang tua?", a: "Ada, tersedia ruang tunggu dengan minuman untuk Ayah dan Bunda." },
    ] },
  },
});
