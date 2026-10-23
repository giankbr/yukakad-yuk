import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Panitia RW 07 Cup", groom: "Karang Taruna Tunas Harapan",
    brideFull: "Panitia Turnamen Futsal RW 07 Cup", groomFull: "Karang Taruna Tunas Harapan RW 07 Sukamaju",
    brideParents: "Bapak-bapak dan pemuda RW 07 yang mengurus jadwal, wasit, konsumsi, dan hadiah. Ketua panitia: Mas Yoga Pratama.",
    groomParents: "Pemuda-pemudi RW 07 yang menyiapkan lapangan, papan skor, dokumentasi, dan siaran langsung di grup warga.",
    note: "Delapan tim, dua hari, satu piala bergilir. Main sportif, pulang tetap tetangga.",
  },
  eventLabel: "Turnamen Futsal RW 07 Cup",
  date: "2027-09-18T07:30:00+07:00",
  place: "GOR Futsal Bina Raga",
  address: "Jl. Cempaka Raya No. 8, Sukamaju, Cilodong, Kota Depok",
  story: { title: "Bagan pertandingan", body: "" },
  stories: [
    { date: "Sabtu · 08.00 · Grup A", title: "RT 01 vs RT 04", body: "Lapangan A. Laga pembuka, dua kali sepuluh menit." },
    { date: "Sabtu · 08.30 · Grup B", title: "RT 02 vs RT 05", body: "Lapangan A. Juara bertahan RT 05 turun lebih dulu." },
    { date: "Sabtu · 10.00 · Grup A", title: "RT 03 vs RT 06", body: "Lapangan B. Dua tim termuda turnamen tahun ini." },
    { date: "Minggu · 09.00 · Semifinal", title: "Juara A vs Runner-up B", body: "Juara grup menghadapi runner-up grup sebelah." },
    { date: "Minggu · 15.30 · Final", title: "Perebutan Piala Bergilir", body: "Pemenang semifinal bertemu di final, disusul penyerahan piala dan hadiah." },
  ],
  events: [
    { name: "Babak Penyisihan Grup", date: "2027-09-18T07:30:00+07:00", time: "07.30 – 16.00 WIB", venue: "GOR Futsal Bina Raga", address: "Jl. Cempaka Raya No. 8, Sukamaju, Cilodong, Kota Depok" },
    { name: "Semifinal, Final & Penyerahan Piala", date: "2027-09-19T09:00:00+07:00", time: "09.00 – 17.00 WIB", venue: "GOR Futsal Bina Raga", address: "Jl. Cempaka Raya No. 8, Sukamaju, Cilodong, Kota Depok" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0391 0100 2287 501", account_name: "Bendahara RW 07 Cup" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "DANA", ewallet_number: "0813 1180 2207", account_name: "Bendahara RW 07 Cup" },
    { id: "demo-barang", type: "address", address: "Sekretariat Karang Taruna, Jl. Cempaka Raya No. 2, Sukamaju, Depok (air mineral, buah, atau hadiah doorprize)" },
  ],
  guestName: "Tim RT 05 Elang Muda",
  guestTable: "Grup B",
  extras: {
    rundown: { items: [
      { time: "07.00", title: "Registrasi tim & technical meeting", note: "Kapten tim membawa daftar pemain" },
      { time: "07.45", title: "Pembukaan oleh Ketua RW 07" },
      { time: "08.00", title: "Kick-off laga pertama" },
      { time: "12.00", title: "Istirahat, salat, & makan siang" },
      { time: "16.00", title: "Pengumuman hasil grup" },
    ] },
    dressCode: { note: "Peserta: seragam tim bernomor dan sepatu futsal sol karet (non-marking). Penonton: bebas, boleh pakai warna tim jagoan.", colors: ["#e8742c", "#2f6db5", "#c6e03a", "#16233f"] },
    guestPass: { note: "Tunjukkan kode ini di meja registrasi untuk mengambil nomor dada dan jadwal tim." },
    family: { names: ["Warung Bu Tini", "Bengkel Jaya Motor", "Toko Olahraga Gol!", "Ikatan Warga RW 07"] },
    faq: { items: [
      { q: "Berapa pemain per tim?", a: "Lima pemain inti dan maksimal lima cadangan, semuanya warga RW 07 atau keluarga yang tinggal di wilayah ini." },
      { q: "Berapa biaya pendaftaran?", a: "Rp150.000 per tim, untuk sewa lapangan, wasit, dan konsumsi pemain. Transfer ke rekening bendahara di bagian Biaya & Donasi." },
      { q: "Boleh datang hanya menonton?", a: "Tentu! Pilih \"Penonton\" saat konfirmasi supaya panitia bisa menyiapkan kursi dan konsumsi." },
    ] },
  },
});
