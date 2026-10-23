import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Raka", groom: "",
    brideFull: "Raka Pradipta Wibowo",
    brideParents: "Putra pertama dari Bapak Dimas Wibowo & Ibu Larasati Putri",
    note: "Chef Raka sudah enam tahun! Pakai celemekmu, kita menghias cupcake dan memanggang pizza mini bersama.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-17T10:00:00+07:00",
  place: "Dapur Ceria Cooking Studio",
  address: "Jl. Kemang Raya No. 23, Bangka, Mampang Prapatan, Jakarta Selatan",
  story: { title: "Resep Raka", body: "" },
  stories: [
    { date: "2021", title: "Adonan pertama", body: "Raka lahir di suatu pagi bulan Juli, wangi kue bolu Eyang memenuhi rumah." },
    { date: "2023", title: "Asisten sendok kayu", body: "Mulai ikut mengaduk adonan pancake hari Minggu bersama Bunda, separuh tepungnya menempel di pipi." },
    { date: "2025", title: "Pemecah telur andal", body: "Bisa memecahkan telur tanpa kulit masuk ke mangkuk. Ayah sampai bertepuk tangan." },
    { date: "2027", title: "Enam tahun, Chef!", body: "Sekarang punya topi koki sendiri dan bercita-cita membuka toko roti." },
  ],
  events: [
    { name: "Pesta Koki Cilik", date: "2027-07-17T10:00:00+07:00", time: "10.00 – 12.30 WIB", venue: "Dapur Ceria Cooking Studio", address: "Jl. Kemang Raya No. 23, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5271 0617 21", account_name: "Larasati Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka XI No. 7, Pela Mampang, Mampang Prapatan, Jakarta Selatan 12720" },
  ],
  guestName: "Adik Bilqis & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Raka Pradipta Wibowo", nickname: "Raka", birthDate: "2021-07-17T07:20:00+07:00", parents: "Putra pertama dari Bapak Dimas Wibowo & Ibu Larasati Putri" },
    rundown: { items: [
      { time: "10.00", title: "Pakai celemek & topi koki", note: "Disediakan di meja penyambutan" },
      { time: "10.30", title: "Menghias cupcake warna-warni" },
      { time: "11.15", title: "Memanggang pizza mini", note: "Didampingi kakak koki studio" },
      { time: "12.00", title: "Tiup lilin & makan bersama" },
    ] },
    dressCode: { note: "Baju nyaman berwarna cerah. Celemek dan topi koki kami siapkan untuk semua teman.", colors: ["#7fcdb4", "#e5533d", "#f6cf5a", "#f6a7bd"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Wibowo", "Kakek & Nenek Sutrisno", "Om Bayu & Tante Rini"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Raka.", items: [
      { id: "w1", name: "Set masak-masakan kayu", price: "± Rp250.000" },
      { id: "w2", name: "Buku resep bergambar untuk anak", price: "± Rp95.000", claimed_by: "Tante Rini" },
      { id: "w3", name: "Celemek & sarung tangan oven mini", price: "± Rp80.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada area duduk dan kopi hangat untuk Ayah & Bunda." },
      { q: "Bagaimana kalau anak punya alergi?", a: "Tuliskan di formulir kehadiran, kami siapkan bahan pengganti." },
    ] },
  },
});
