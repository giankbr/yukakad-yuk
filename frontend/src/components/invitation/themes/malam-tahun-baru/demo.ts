import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Raka & Sasha", groom: "",
    brideFull: "Raka Aditya & Sasha Paramitha",
    brideParents: "Tuan rumah malam ini,\nbersama anak-anak Kontrakan Tebet",
    note: "Satu tahun lagi selesai. Kita tutup bareng di atap, dengan jagung bakar, playlist kebanyakan lagu lama, dan langit yang penuh kembang api.",
  },
  eventLabel: "Malam Tahun Baru",
  // Countdown runs to the last second of 2027 (00.00 WIB on 1 Januari 2028) while the date still reads 31 Desember.
  date: "2027-12-31T23:59:59+07:00",
  place: "Rooftop Wisma Kenari",
  address: "Jl. Tebet Barat Dalam IV No. 21, Tebet, Jakarta Selatan",
  story: { title: "Tradisi kami", body: "" },
  stories: [
    { date: "2021", title: "Atap pertama", body: "Berlima, satu panggangan pinjaman, dan kembang api yang kami tonton dari kejauhan. Tradisi kecil ini dimulai tanpa rencana." },
    { date: "2024", title: "Makin ramai", body: "Tetangga lantai bawah ikut naik, ada yang membawa gitar, ada yang membawa martabak. Hitung mundur kami teriakkan bersama-sama." },
    { date: "2027", title: "Edisi ketujuh", body: "Tahun ini kami siapkan lebih serius: lampu gantung, meja panjang, dan pemandangan langit Jakarta dari sudut terbaik." },
  ],
  events: [
    { name: "Kumpul & Makan Malam", date: "2027-12-31T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Rooftop Wisma Kenari", address: "Jl. Tebet Barat Dalam IV No. 21, Tebet, Jakarta Selatan" },
    { name: "Hitung Mundur & Kembang Api", date: "2027-12-31T23:30:00+07:00", time: "23.30 – 00.30 WIB", venue: "Rooftop Wisma Kenari", address: "Jl. Tebet Barat Dalam IV No. 21, Tebet, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a137.webp", "/themes/img/a129.webp", "/themes/img/r0.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Jago", account_number: "1027 3348 0091", account_name: "Sasha Paramitha (Bendahara Patungan)" },
  ],
  guestName: "Bimo & Partner",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "19.00", title: "Datang & bakar-bakar", note: "Jagung, sosis, dan sate taichan" },
      { time: "21.00", title: "Kuis tahunan & tukar kado", note: "Kado maksimal Rp50.000" },
      { time: "23.30", title: "Kumpul di sisi timur atap" },
      { time: "00.00", title: "Hitung mundur & kembang api" },
    ] },
    dressCode: { note: "Kilau sedikit boleh, nyaman itu wajib. Emas, hitam, atau warna apa pun yang bikin semangat. Bawa jaket tipis, angin di atap lumayan.", colors: ["#e6bf6e", "#082029", "#ff6f61", "#7fe3c8"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Boleh ajak teman?", a: "Boleh, kabari dulu lewat konfirmasi supaya makanannya cukup." },
      { q: "Ada parkir?", a: "Parkir motor di halaman, mobil di sepanjang jalan. Lebih aman naik ojek atau KRL ke Stasiun Tebet." },
      { q: "Pulangnya bagaimana?", a: "Acara selesai sekitar pukul 00.30. Kami bantu pesankan kendaraan kalau perlu." },
    ] },
  },
});
