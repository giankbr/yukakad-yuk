import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Danish", groom: "",
    brideFull: "Danish Arkana Pratama",
    brideParents: "Putra kedua dari Bapak Yoga Pratama & Ibu Mega Lestari",
    note: "Danish genap enam tahun! Ayo datang, kita hias donat sendiri, tabur meses sebanyak-banyaknya, lalu tumpuk jadi kue paling tinggi.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-05-22T15:00:00+07:00",
  place: "Kedai Donat Gula Kapas",
  address: "Jl. Cipete Raya No. 27B, Cipete Selatan, Cilandak, Jakarta Selatan",
  story: { title: "Cerita Danish", body: "" },
  stories: [
    { date: "2021", title: "Bayi bulat di bulan Mei", body: "Danish lahir di pagi yang cerah. Kata Bunda, pipinya bulat seperti donat yang baru keluar dari penggorengan." },
    { date: "2024", title: "Donat pertama", body: "Donat cokelat pertama Danish berakhir separuh di mulut dan separuh di lantai. Meses menempel sampai ke rambut." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang Danish sudah bisa menghias donat sendiri: glasir stroberi, meses pelangi, dan satu permen di tengah." },
  ],
  events: [
    { name: "Pesta Donat Danish", date: "2027-05-22T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Kedai Donat Gula Kapas", address: "Jl. Cipete Raya No. 27B, Cipete Selatan, Cilandak, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5270 2205 2027", account_name: "Mega Lestari" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Selatan VIII No. 14, Bangka, Mampang Prapatan, Jakarta Selatan 12730" },
  ],
  guestName: "Adik Kayla & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Danish Arkana Pratama", nickname: "Danish", birthDate: "2021-05-19T07:40:00+07:00", parents: "Putra kedua dari Bapak Yoga Pratama & Ibu Mega Lestari" },
    rundown: { items: [
      { time: "15.00", title: "Datang & pilih topi koki", note: "Setiap anak dapat celemek mini" },
      { time: "15.20", title: "Menghias donat sendiri", note: "Glasir stroberi, cokelat, vanila, dan meses pelangi" },
      { time: "16.15", title: "Lomba menara donat tertinggi" },
      { time: "17.00", title: "Tiup lilin di kue donat & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju warna glasir kesukaanmu: stroberi, mint, vanila, cokelat, atau ungu!", colors: ["#f58fb3", "#9fe3c9", "#fff1c9", "#6e3b2a", "#c8adf2"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi telur, susu, kacang, atau makanan lain pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Eyang Uti Lestari", "Kak Nara"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini yang sedang Danish impikan.", items: [
      { id: "w1", name: "Set mainan toko roti kayu", price: "± Rp200.000" },
      { id: "w2", name: "Buku cerita bergambar dinosaurus", price: "± Rp85.000", claimed_by: "Om Bima" },
      { id: "w3", name: "Celemek & topi koki anak", price: "± Rp70.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu. Ada area duduk untuk orang tua lengkap dengan kopi, teh, dan donat untuk orang dewasa." },
      { q: "Ada pilihan untuk anak yang alergi?", a: "Ada! Kami menyiapkan donat tanpa telur dan tanpa susu. Mohon tuliskan di form konfirmasi." },
    ] },
  },
});
