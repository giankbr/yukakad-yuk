import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Clara", groom: "Bastian",
    brideFull: "Clara Anindita Wibisono", groomFull: "Bastian Raditya Halim",
    brideParents: "Putri tunggal dari\nBapak Hendro Wibisono & Ibu Lily Tanoto", groomParents: "Putra kedua dari\nBapak Arief Halim & Ibu Maria Kurniawati",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Kami pernah menunggu cahaya utara semalaman di tepi danau beku. Kini kami menunggu Anda, di hari yang kami nantikan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-12-18T15:00:00+07:00",
  place: "Hutan Pinus Cikole",
  address: "Jl. Raya Tangkuban Perahu KM 2,5, Cikole, Lembang, Kabupaten Bandung Barat",
  story: { title: "", body: "" },
  stories: [
    { date: "Februari 2022", title: "Malam Paling Dingin", body: "Dua rombongan wisata dari Jakarta terjebak menunggu aurora di Tromsø. Bastian meminjamkan termos cokelat panasnya, dan kami mengobrol sampai langit menyala hijau." },
    { date: "2023 – 2025", title: "Dua Kota, Satu Langit", body: "Clara di Bandung, Bastian di Jakarta. Setiap Jumat malam kami menelepon sambil melihat bintang dari jendela masing-masing." },
    { date: "Januari 2027", title: "Di Tepi Danau", body: "Bastian melamar di tepi danau beku tempat kami pertama bertemu, tepat saat aurora muncul untuk kedua kalinya." },
  ],
  events: [
    { name: "Ikrar Pernikahan", date: "2027-12-18T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Hutan Pinus Cikole", address: "Jl. Raya Tangkuban Perahu KM 2,5, Cikole, Lembang, Kabupaten Bandung Barat" },
    { name: "Resepsi Malam", date: "2027-12-18T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Paviliun Kaca Cikole", address: "Jl. Raya Tangkuban Perahu KM 2,5, Cikole, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/r89.webp", "/themes/img/r104.webp", "/themes/img/r102.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 8812 09", account_name: "Clara Anindita Wibisono" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1320 0477 1185", account_name: "Bastian Raditya Halim" },
    { id: "demo-kado", type: "address", address: "Jl. Dago Pakar Timur No. 9, Ciburial, Cimenyan, Kabupaten Bandung 40198" },
  ],
  guestName: "Bapak Yosef Hartanto & Keluarga",
  guestTable: "Meja Pinus 4",
  extras: {
    quote: { text: "Cinta tidak saling memandang satu sama lain, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "15.00", title: "Ikrar pernikahan di bawah pinus" },
      { time: "16.00", title: "Teh hangat & foto bersama" },
      { time: "18.30", title: "Resepsi malam dibuka", note: "Paviliun Kaca" },
      { time: "20.00", title: "Pesta dansa & api unggun" },
    ] },
    dressCode: { note: "Hangat dan rapi: rajut, wol, atau mantel bernuansa biru malam, hijau pinus, dan ungu senja. Lembang cukup dingin selepas magrib.", colors: ["#0d1a2b", "#2f5d50", "#6b5ba8", "#e8f0f5"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendro Wibisono", "Kel. Besar Bpk. Arief Halim"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan terdekat dari lokasi.", items: [
      { name: "Shuttle dari Dago", detail: "Berangkat 13.30 dan 17.30 dari Taman Hutan Raya Djuanda" },
      { name: "Parkir", detail: "Parkir mobil di area depan Hutan Pinus Cikole, jalan kaki 3 menit" },
    ] },
    faq: { items: [
      { q: "Apakah acaranya di luar ruangan?", a: "Ikrar di bawah pinus (luar ruangan, tersedia tenda), resepsi di paviliun kaca tertutup." },
      { q: "Boleh membawa anak?", a: "Tentu. Jangan lupa jaket hangat untuk si kecil." },
    ] },
  },
});
