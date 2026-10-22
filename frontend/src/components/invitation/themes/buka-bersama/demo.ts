import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alumni Smansa '12", groom: "",
    brideFull: "Ikatan Alumni SMA Negeri 3 Bandung Angkatan 2012",
    brideParents: "Panitia: Rizky Ramadhan, Nadia Putri & Fajar Hidayat",
    note: "Lima belas tahun selepas seragam putih abu-abu, mari kembali duduk semeja: berbuka, bershalat jamaah, dan berbagi dengan adik-adik panti.",
  },
  eventLabel: "Buka Bersama",
  date: "2027-02-20T17:30:00+07:00",
  place: "Aula SMA Negeri 3 Bandung",
  address: "Jl. Belitung No. 8, Merdeka, Sumur Bandung, Kota Bandung",
  story: { title: "", body: "" },
  stories: [
    { date: "Juni 2012", title: "Lulus Bersama", body: "Dua ratus delapan puluh siswa melempar topi di lapangan basket. Janji kami: bertemu lagi setiap Ramadan." },
    { date: "Ramadan 2019", title: "Bukber Pertama", body: "Baru dua puluh orang yang datang ke warung kopi dekat sekolah. Kurmanya kurang, tapi ceritanya tidak habis-habis." },
    { date: "Ramadan 2026", title: "Santunan Perdana", body: "Iuran angkatan pertama kali kami sisihkan untuk santunan 40 anak Panti Asuhan Al-Hikmah Cicadas." },
  ],
  events: [
    { name: "Kajian Singkat & Buka Bersama", date: "2027-02-20T17:30:00+07:00", time: "17.30 – 18.45 WIB", venue: "Aula SMA Negeri 3 Bandung", address: "Jl. Belitung No. 8, Merdeka, Sumur Bandung, Kota Bandung" },
    { name: "Shalat Isya & Tarawih Berjamaah", date: "2027-02-20T19:20:00+07:00", time: "19.20 WIB – selesai", venue: "Masjid Al-Hikmah SMAN 3 Bandung", address: "Jl. Belitung No. 8, Merdeka, Sumur Bandung, Kota Bandung" },
  ],
  gallery: ["/themes/img/r19.webp", "/themes/img/r59.webp", "/themes/img/r63.webp", "/themes/img/r20.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 4433 18", account_name: "Fajar Hidayat (Bendahara)" },
  ],
  guestName: "Sdr. Dimas Pratama",
  guestTable: "Meja 7",
  extras: {
    quote: { text: "Barang siapa memberi makan orang yang berpuasa, maka baginya pahala seperti orang yang berpuasa itu, tanpa mengurangi pahala orang yang berpuasa sedikit pun.", source: "HR. At-Tirmidzi" },
    rundown: { items: [
      { time: "17.30", title: "Registrasi & kajian singkat", note: "Ustaz Hilman Fauzi (alumni 2012)" },
      { time: "18.14", title: "Azan magrib, takjil kurma & es teh" },
      { time: "18.25", title: "Shalat magrib berjamaah" },
      { time: "18.45", title: "Makan bersama & kabar angkatan" },
      { time: "19.05", title: "Santunan anak yatim", note: "Panti Asuhan Al-Hikmah Cicadas" },
      { time: "19.20", title: "Shalat isya & tarawih" },
    ] },
    dressCode: { note: "Busana muslim santai. Yang masih menyimpan kaos angkatan, ayo dipakai lagi!", colors: ["#5b2c4a", "#d4a243", "#2f6b5a", "#fbf3e6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Panitia Bukber", names: ["Rizky Ramadhan (Ketua)", "Nadia Putri (Acara)", "Fajar Hidayat (Bendahara)", "Siti Aulia (Konsumsi)"] },
    faq: { items: [
      { q: "Berapa iuran bukbernya?", a: "Rp150.000 per orang, sudah termasuk takjil, makan malam, dan sumbangan santunan." },
      { q: "Boleh membawa keluarga?", a: "Boleh, cukup isi jumlah tamu saat konfirmasi agar panitia bisa menyiapkan porsi." },
      { q: "Di mana parkir?", a: "Parkir motor di halaman sekolah, mobil di sepanjang Jl. Belitung dan Jl. Sumbawa." },
    ] },
  },
});
