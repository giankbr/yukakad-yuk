import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Panitia Piala Benteng", groom: "Klub Catur Kuda Hitam",
    brideFull: "Panitia Turnamen Catur Piala Benteng RW 09", groomFull: "Klub Catur Kuda Hitam Tlogosari",
    brideParents: "Bapak-bapak dan pemuda RW 09 yang mengurus papan, jam catur, pairing, konsumsi, dan hadiah. Ketua panitia: Pak Bambang Sutrisno.",
    groomParents: "Klub catur warga yang berlatih tiap Kamis malam di pos ronda. Menyiapkan arbiter, papan peraga, dan siaran hasil di grup warga.",
    note: "Lima babak sistem Swiss, satu piala bergilir, dan teh hangat untuk semua pemain.",
  },
  eventLabel: "Turnamen Catur Piala Benteng",
  date: "2027-11-13T08:00:00+07:00",
  place: "Balai Warga RW 09",
  address: "Jl. Kenari Raya No. 14, Tlogosari Kulon, Pedurungan, Kota Semarang",
  story: { title: "Jadwal turnamen", body: "" },
  stories: [
    { date: "Sabtu · 08.30 · Babak 1", title: "Pembukaan & babak pertama", body: "Pairing acak per kategori. Rapid 15 menit + 5 detik per langkah." },
    { date: "Sabtu · 10.00 · Babak 2", title: "Babak kedua", body: "Pemain dengan poin sama dipertemukan. Hasil diumumkan di papan pengumuman." },
    { date: "Sabtu · 13.00 · Babak 3", title: "Babak ketiga", body: "Setelah istirahat, salat, dan makan siang. Papan 1–3 jadi papan peraga untuk penonton." },
    { date: "Minggu · 08.30 · Babak 4–5", title: "Penentuan klasemen", body: "Dua babak terakhir menentukan juara umum, juara pelajar, dan pemain terbaik RW." },
    { date: "Minggu · 13.30 · Final", title: "Penyerahan Piala Bergilir", body: "Simultan bersama juara bertahan, lalu penyerahan piala, medali, dan doorprize." },
  ],
  events: [
    { name: "Babak 1–3 (Sistem Swiss)", date: "2027-11-13T08:00:00+07:00", time: "08.00 – 16.00 WIB", venue: "Balai Warga RW 09", address: "Jl. Kenari Raya No. 14, Tlogosari Kulon, Pedurungan, Kota Semarang" },
    { name: "Babak 4–5 & Penyerahan Piala", date: "2027-11-14T08:00:00+07:00", time: "08.00 – 15.00 WIB", venue: "Balai Warga RW 09", address: "Jl. Kenari Raya No. 14, Tlogosari Kulon, Pedurungan, Kota Semarang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0217 0100 4471 509", account_name: "Bendahara Piala Benteng" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "DANA", ewallet_number: "0857 4011 2093", account_name: "Bendahara Piala Benteng" },
    { id: "demo-barang", type: "address", address: "Sekretariat Klub Kuda Hitam, Jl. Kenari Raya No. 2, Tlogosari Kulon, Semarang (buku catur, papan, atau hadiah doorprize)" },
  ],
  guestName: "Mas Rendra Saputra",
  guestTable: "Papan 7",
  extras: {
    rundown: { items: [
      { time: "07.30", title: "Daftar ulang & ambil nomor papan", note: "Bawa kartu pelajar untuk kategori pelajar" },
      { time: "08.15", title: "Pembukaan oleh Ketua RW 09" },
      { time: "08.30", title: "Babak 1 dimulai", note: "Jam catur dijalankan bersamaan" },
      { time: "12.00", title: "Istirahat, salat, & makan siang" },
      { time: "16.00", title: "Klasemen sementara diumumkan" },
    ] },
    guestPass: { note: "Tunjukkan kode ini di meja arbiter untuk mengambil nomor papan dan formulir notasi." },
    family: { title: "Didukung oleh", names: ["Toko Buku Pelangi", "Warung Kopi Pak Darmo", "Percetakan Sinar Jaya", "Ikatan Warga RW 09"] },
    faq: { items: [
      { q: "Siapa yang boleh ikut?", a: "Warga RW 09 dan sekitarnya, semua umur. Ada kategori umum dan kategori pelajar (SD–SMA)." },
      { q: "Berapa biaya pendaftarannya?", a: "Rp25.000 untuk kategori umum dan Rp10.000 untuk pelajar, sudah termasuk konsumsi dan formulir notasi." },
      { q: "Perlu bawa papan sendiri?", a: "Tidak perlu. Panitia menyiapkan papan dan jam catur. Penonton dimohon tenang di area permainan." },
    ] },
  },
});
