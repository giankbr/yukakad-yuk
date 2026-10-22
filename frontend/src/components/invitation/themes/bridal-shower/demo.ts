import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "",
    brideFull: "Nadia Paramitha Wirawan",
    brideParents: "Calon istri dari Adrian Wicaksono\nMenikah 18 September 2027",
    bridePhoto: "/themes/img/r27.webp",
    note: "Sebelum Nadia resmi melepas masa lajang, yuk manjakan dia seharian: brunch cantik, permainan seru, dan pelukan dari para sahabat.",
  },
  eventLabel: "Bridal Shower",
  date: "2027-08-28T10:30:00+07:00",
  place: "Teras Kebun Dago",
  address: "Jl. Ir. H. Juanda No. 210, Dago, Coblong, Kota Bandung",
  story: { title: "", body: "" },
  stories: [
    { date: "2016", title: "Sekamar di asrama", body: "Kami bertemu Nadia di asrama mahasiswi. Dia yang selalu membangunkan semua orang untuk kuliah pagi." },
    { date: "2024", title: "Bertemu Adrian", body: "Di acara pernikahan sahabat, Nadia kebagian duduk semeja dengan seorang arsitek yang pandai melucu." },
    { date: "2027", title: "Bilang \"iya\"", body: "Adrian melamar di kebun teh Ciwidey. Nadia menangis, kami semua ikut menangis di grup chat." },
  ],
  events: [
    { name: "Brunch & Bridal Shower", date: "2027-08-28T10:30:00+07:00", time: "10.30 – 14.00 WIB", venue: "Teras Kebun Dago", address: "Jl. Ir. H. Juanda No. 210, Dago, Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/r79.webp", "/themes/img/r28.webp", "/themes/img/r3.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 2281 66", account_name: "Kirana Larasati" },
  ],
  guestName: "Tasya Amelia",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "10.30", title: "Welcome mocktail & photobooth", note: "Ambil selempang dan bunga rambutmu" },
      { time: "11.15", title: "Brunch bersama" },
      { time: "12.15", title: "Kuis: seberapa kenal kamu dengan Nadia?", note: "Hadiah untuk pemenang" },
      { time: "13.15", title: "Membuka kado & surat untuk sang bride" },
    ] },
    dressCode: { note: "Nuansa lembut: blush pink, putih, champagne, atau hijau sage. Dress, rok, atau gamis, semuanya cantik.", colors: ["#f6c9d0", "#fffaf6", "#f1d3b8", "#a9bf9a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Tuan Rumah", names: ["Kirana Larasati (Maid of Honor)", "Tasya & Dinda", "Laras, Sekar & Meisya"] },
    wishlist: { note: "Kehadiranmu sudah jadi hadiah terbaik. Kalau ingin ikut memberi, ini daftar kecil dari kami untuk Nadia.", items: [
      { id: "w1", name: "Set piyama satin", price: "± Rp350.000" },
      { id: "w2", name: "Set wadah bumbu keramik", price: "± Rp280.000", claimed_by: "Dinda" },
      { id: "w3", name: "Voucher spa & pijat", price: "± Rp500.000" },
    ] },
    faq: { items: [
      { q: "Apakah calon pengantin pria ikut hadir?", a: "Acara ini khusus para sahabat perempuan. Adrian baru datang menjemput Nadia di akhir acara." },
      { q: "Perlu membawa kado?", a: "Tidak wajib. Surat pendek berisi doa dan nasihat untuk Nadia justru paling kami tunggu." },
    ] },
  },
});
