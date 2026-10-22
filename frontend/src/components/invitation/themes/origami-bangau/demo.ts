import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Angeline", groom: "Kevin",
    brideFull: "Angeline Wijaya, S.Psi.", groomFull: "Kevin Tanoto, S.Kom.",
    brideParents: "Putri kedua dari\nBapak Hendra Wijaya & Ibu Lanny Susanto",
    groomParents: "Putra pertama dari\nBapak Budi Tanoto & Ibu Melinda Gozali",
    note: "Seribu bangau kertas kami lipat bersama, satu per satu, untuk satu harapan: hidup panjang yang saling menjaga.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T09:00:00+07:00",
  place: "Vihara Ekayana Arama",
  address: "Jl. Mangga II No. 8, Duri Kepa, Kebon Jeruk, Jakarta Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2018", title: "Kelas Origami", body: "Kevin datang ke kelas origami di perpustakaan kota karena salah membaca jadwal. Angeline mengajarinya melipat bangau pertamanya." },
    { date: "2021", title: "Seratus Bangau", body: "Selama Angeline menyelesaikan skripsi, Kevin mengirim satu bangau kertas setiap hari, lengkap dengan catatan kecil di sayapnya." },
    { date: "2026", title: "Bangau Keseribu", body: "Di bangau keseribu tertulis sebuah pertanyaan. Jawabannya: ya." },
  ],
  events: [
    { name: "Pemberkatan Pernikahan", date: "2027-09-18T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Vihara Ekayana Arama", address: "Jl. Mangga II No. 8, Duri Kepa, Kebon Jeruk, Jakarta Barat" },
    { name: "Resepsi", date: "2027-09-18T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Hotel Santika Premiere Slipi", address: "Jl. Aipda K.S. Tubun No. 7, Slipi, Palmerah, Jakarta Barat" },
  ],
  gallery: ["/themes/img/a78.webp", "/themes/img/a125.webp", "/themes/img/a18.webp", "/themes/img/a117.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4410 2287 19", account_name: "Angeline Wijaya" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0812 9087 6543", account_name: "Kevin Tanoto" },
  ],
  guestName: "Ibu Susi Halim & Keluarga",
  guestTable: "Meja Bangau 9",
  extras: {
    quote: { text: "Bangau kertas tidak pernah selesai dalam satu lipatan. Begitu pula cinta: dirawat dengan sabar, satu lipatan setiap hari.", source: "Angeline & Kevin" },
    rundown: { items: [
      { time: "18.30", title: "Penerimaan tamu", note: "Tulis harapan di bangau kertas" },
      { time: "19.00", title: "Masuknya pengantin" },
      { time: "19.30", title: "Makan malam" },
      { time: "20.15", title: "Senbazuru: menggantung seribu bangau", note: "Bersama keluarga dan sahabat" },
    ] },
    dressCode: { note: "Warna pastel lembut: merah muda, mint, kuning mentega, atau lilac.", colors: ["#f0b5ae", "#b9e0cf", "#f5e0a0", "#cbbdec"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Wijaya", "Kel. Besar Bpk. Budi Tanoto"] },
    travel: { note: "Untuk tamu dari luar kota, berikut info yang mungkin membantu.", items: [
      { name: "Menginap", detail: "Tersedia kamar dengan harga khusus di hotel resepsi" },
      { name: "Parkir", detail: "Parkir vihara terbatas, disarankan memakai taksi daring" },
    ] },
    wishlist: { items: [
      { id: "w1", name: "Set teko & cangkir teh", price: "± Rp450.000" },
      { id: "w2", name: "Kertas washi untuk origami", price: "± Rp150.000", claimed_by: "Cici Fenny" },
      { id: "w3", name: "Tabungan bulan madu", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh hadir di pemberkatan?", a: "Boleh. Mohon berpakaian sopan dan melepas alas kaki di area Dhammasala." },
      { q: "Sampai jam berapa resepsinya?", a: "Resepsi berlangsung hingga pukul 21.00 WIB." },
    ] },
  },
});
