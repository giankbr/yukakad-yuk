import { makeDemo } from "../demo-base";

// Ulang tahun anak bertema tukang kebun cilik: menanam bibit, menyiram, dan memetik sayur di kebun edukasi Kota Batu.
export const demo = makeDemo({
  couple: {
    bride: "Naya", groom: "",
    brideFull: "Kanaya Putri Lestari",
    brideParents: "Putri kedua dari Bapak Arief Wicaksono & Ibu Dian Lestari",
    note: "Naya sudah lima tahun! Ayo pakai topi kebunmu, kita menanam, menyiram, dan memetik wortel bersama.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-10T09:00:00+07:00",
  place: "Kebun Edukasi Tunas Mekar",
  address: "Jl. Raya Batu–Malang Km. 7, Beji, Junrejo, Kota Batu",
  story: { title: "Buku Tanam Naya", body: "" },
  stories: [
    { date: "2022", title: "Benih kecil", body: "Naya lahir di bulan Juli, mungil dan hangat seperti benih yang baru ditanam." },
    { date: "2024", title: "Tomat pertama", body: "Memetik tomat ceri dari pot di teras rumah, lalu dimakan semuanya sebelum sampai dapur." },
    { date: "2026", title: "Penyiram setia", body: "Setiap pagi menyirami pot bunga Bunda dengan gembor hijau kesayangannya." },
    { date: "2027", title: "Tukang kebun lima tahun", body: "Sekarang sudah hafal nama sayur dan tahu cacing tanah itu teman kebun." },
  ],
  events: [
    { name: "Pesta Kebun Naya", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 11.30 WIB", venue: "Kebun Edukasi Tunas Mekar", address: "Jl. Raya Batu–Malang Km. 7, Beji, Junrejo, Kota Batu" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0123 0110 2207 503", account_name: "Dian Lestari" },
    { id: "demo-kado", type: "address", address: "Perum Griya Asri Blok C-12, Sisir, Kec. Batu, Kota Batu 65314" },
  ],
  guestName: "Adik Raka & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kanaya Putri Lestari", nickname: "Naya", birthDate: "2022-07-10T06:40:00+07:00", parents: "Putri kedua dari Bapak Arief Wicaksono & Ibu Dian Lestari" },
    quote: { text: "Tanamlah kebaikan sejak kecil, rawatlah dengan sabar, nanti ia tumbuh jadi kebun yang penuh warna.", source: "Ayah & Bunda" },
    rundown: { items: [
      { time: "09.00", title: "Pakai topi & celemek kebun", note: "Disediakan untuk semua tukang kebun cilik" },
      { time: "09.30", title: "Menanam bibit di pot", note: "Potnya boleh dibawa pulang" },
      { time: "10.15", title: "Memetik wortel & tomat" },
      { time: "10.45", title: "Tiup lilin kue wortel & makan bersama" },
    ] },
    dressCode: { note: "Baju yang boleh kena tanah! Warna hijau daun, oranye wortel, atau merah tomat.", colors: ["#6fa04a", "#f08a2c", "#e2493a", "#f6efe0"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Wicaksono", "Mbah Kakung & Mbah Putri Lestari"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Naya.", items: [
      { id: "w1", name: "Set alat berkebun anak", price: "± Rp150.000" },
      { id: "w2", name: "Buku cerita tentang sayuran", price: "± Rp85.000", claimed_by: "Tante Sari" },
      { id: "w3", name: "Sepatu bot karet hijau", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Perlu membawa baju ganti?", a: "Boleh sekali, karena kita akan bermain tanah dan menyiram tanaman." },
      { q: "Apakah orang tua boleh ikut?", a: "Tentu! Ada saung teduh untuk Ayah dan Bunda sambil menemani." },
    ] },
  },
});
