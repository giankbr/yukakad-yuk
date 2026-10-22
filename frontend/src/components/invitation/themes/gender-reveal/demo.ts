import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Dinda", groom: "Arya",
    brideFull: "Adinda Kirana Putri",
    groomFull: "Arya Bimantara",
    brideParents: "Calon bunda, sedang di trimester kedua",
    groomParents: "Calon ayah, sudah belajar memasang popok",
    note: "Si kecil sudah 20 minggu di perut dan pandai menyembunyikan rahasianya. Hanya dokter dan sebuah kotak balon yang tahu. Yuk, buka bersama kami!",
  },
  eventLabel: "Gender Reveal",
  date: "2027-03-14T15:30:00+07:00",
  place: "Halaman Belakang Rumah Keluarga Bimantara",
  address: "Jl. Bukit Pakar Timur No. 23, Ciburial, Cimenyan, Bandung",
  story: { title: "Kabar kecil kami", body: "" },
  stories: [
    { date: "Oktober 2026", title: "Dua garis", body: "Dinda menyembunyikan test pack di kotak sepatu baru untuk Arya. Arya mengira itu cuma sepatu, sampai ia membukanya." },
    { date: "Desember 2026", title: "Detak pertama", body: "Mendengar detak jantung si kecil untuk pertama kali. Arya merekamnya dan memutarnya setiap malam." },
    { date: "Februari 2027", title: "Amplop rahasia", body: "Dokter menuliskan jawabannya di amplop tertutup. Kami menitipkannya ke Tante Rina, yang menyiapkan kotak balonnya." },
  ],
  events: [
    { name: "Pesta Gender Reveal", date: "2027-03-14T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Halaman Belakang Rumah Keluarga Bimantara", address: "Jl. Bukit Pakar Timur No. 23, Ciburial, Cimenyan, Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "131 00 2210 5567", account_name: "Adinda Kirana Putri" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0813 2045 7781", account_name: "Arya Bimantara" },
  ],
  guestName: "Om Fajar & Tante Mira",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "15.30", title: "Datang & pilih tim", note: "Pita biru atau pita pink di meja depan" },
      { time: "16.00", title: "Tebak-tebakan & permainan", note: "Hadiah untuk tebakan paling meyakinkan" },
      { time: "16.45", title: "Hitung mundur & buka kotak balon" },
      { time: "17.00", title: "Makan sore & foto bersama" },
    ] },
    dressCode: { note: "Pakai warna tebakanmu: biru untuk tim cowok, merah muda untuk tim cewek.", colors: ["#7db4e0", "#f2a0bc", "#fff7ee", "#ffd56b"] },
    guestPass: {},
    rsvpDietary: {},
    wishlist: { note: "Kehadiranmu sudah cukup! Kalau ingin memberi, ini yang masih kami cari (warna netral, aman untuk tim mana pun).", items: [
      { id: "w1", name: "Gendongan bayi ergonomis", price: "± Rp450.000" },
      { id: "w2", name: "Set baju bayi warna krem (0–3 bulan)", price: "± Rp180.000", claimed_by: "Tante Rina" },
      { id: "w3", name: "Lampu tidur proyektor bintang", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Boleh bawa anak-anak?", a: "Boleh banget. Ada sudut gambar dan gelembung sabun untuk mereka." },
      { q: "Kalau hujan?", a: "Acara pindah ke ruang keluarga di dalam rumah. Kotak balonnya tetap dibuka!" },
    ] },
  },
});
