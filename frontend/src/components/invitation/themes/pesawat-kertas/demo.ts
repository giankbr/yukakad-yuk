import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinan", groom: "Gilang",
    brideFull: "Kinanti Ayu Maharani", groomFull: "Gilang Pramudya Saputra",
    brideParents: "Putri bungsu dari\nBapak Andi Rahmat & Ibu Sri Wahyuni",
    groomParents: "Putra pertama dari\nBapak Yohanes Saputra & Ibu Desi Natalia",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Tiga tahun, dua kota, ratusan pesan yang terbang bolak-balik. Kali ini kami mendarat di tempat yang sama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T10:00:00+08:00",
  place: "Gedung Pertemuan Anging Mammiri",
  address: "Jl. Penghibur No. 18, Losari, Kec. Ujung Pandang, Kota Makassar",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2023", title: "Kursi 14A dan 14B", body: "Penerbangan Jakarta – Makassar yang tertunda dua jam. Kinan meminjam pulpen, Gilang meminjamkan bahu untuk tidur." },
    { date: "2024", title: "Surat yang Dilipat", body: "Kami berjanji saling mengirim satu catatan tiap minggu. Kinan selalu melipatnya jadi pesawat kertas." },
    { date: "2026", title: "Satu Tiket Pulang", body: "Gilang pindah tugas ke Makassar dan melamar di pantai Losari, dengan pesawat kertas berisi satu pertanyaan." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-08-14T10:00:00+08:00", time: "10.00 – 11.30 WITA", venue: "Gedung Pertemuan Anging Mammiri", address: "Jl. Penghibur No. 18, Losari, Kec. Ujung Pandang, Kota Makassar" },
    { name: "Resepsi", date: "2027-08-14T18:30:00+08:00", time: "18.30 – 21.00 WITA", venue: "Taman Atap Anging Mammiri", address: "Lantai 4, Jl. Penghibur No. 18, Kota Makassar" },
  ],
  gallery: ["/themes/img/r37.webp", "/themes/img/r11.webp", "/themes/img/a123.webp", "/themes/img/r42.webp", "/themes/img/r14.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "152 00 4471 2093", account_name: "Kinanti Ayu Maharani" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0852 4210 3381", account_name: "Gilang Pramudya Saputra" },
  ],
  guestName: "Kak Meyliana & Partner",
  guestTable: "Meja Awan 6",
  extras: {
    quote: { text: "Sejauh apa pun jaraknya, selalu ada angin yang membawa pulang.", source: "Kinan & Gilang" },
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Keluarga & sahabat dekat" },
      { time: "18.30", title: "Resepsi dibuka" },
      { time: "19.30", title: "Lomba pesawat kertas", note: "Hadiah untuk yang terbang paling jauh" },
      { time: "20.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Santai rapi dengan warna langit: biru muda, putih, dan aksen merah.", colors: ["#bfe0f4", "#2e64b0", "#fbfaf5", "#d9493b"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Andi Rahmat", "Kel. Besar Bpk. Yohanes Saputra"] },
    travel: { note: "Untuk tamu yang terbang dari luar kota, berikut info singkat.", items: [
      { name: "Bandara Sultan Hasanuddin", detail: "± 35 menit ke lokasi via tol" },
      { name: "Hotel terdekat", detail: "Kawasan Pantai Losari, jalan kaki 5 menit" },
    ] },
  },
});
