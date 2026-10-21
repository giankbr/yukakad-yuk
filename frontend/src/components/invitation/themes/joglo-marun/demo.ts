import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Bayu",
    brideFull: "Laras Ayu Pramesti, S.Sn.", groomFull: "Bayu Adi Nugroho, S.T.",
    brideParents: "Putri kedua dari\nBapak Drs. Sutrisno Hadi & Ibu Endang Lestari", groomParents: "Putra sulung dari\nBapak Agus Prasetyo & Ibu Sri Wahyuni",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Witing tresna jalaran saka kulina — cinta tumbuh karena terbiasa bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T08:00:00+07:00",
  place: "Pendhapa Sasana Mulya",
  address: "Jl. Gajahan No. 1, Baluwarti, Pasar Kliwon, Kota Surakarta",
  stories: [
    { date: "2018", title: "Kenal di Sanggar", body: "Laras menari, Bayu memainkan kendang di sanggar karawitan kampus. Satu pentas, lalu banyak latihan bersama." },
    { date: "2022", title: "Saling Menjaga", body: "Jarak Solo–Jakarta tidak membuat kami berhenti. Setiap pulang, kami selalu kembali ke angkringan yang sama." },
    { date: "2026", title: "Nontoni & Lamaran", body: "Keluarga Bayu datang ke rumah dengan seserahan sederhana, disambut hangat keluarga besar Laras." },
  ],
  events: [
    { name: "Siraman & Midodareni", date: "2027-06-18T09:00:00+07:00", time: "09.00 WIB – selesai", venue: "Ndalem Kediaman Mempelai Putri", address: "Jl. Slamet Riyadi No. 214, Laweyan, Kota Surakarta" },
    { name: "Ijab Kabul", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Pendhapa Sasana Mulya", address: "Jl. Gajahan No. 1, Baluwarti, Pasar Kliwon, Kota Surakarta" },
    { name: "Panggih & Resepsi", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendhapa Sasana Mulya", address: "Jl. Gajahan No. 1, Baluwarti, Pasar Kliwon, Kota Surakarta" },
  ],
  gallery: ["/themes/img/a24.webp", "/themes/img/a46.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a34.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0154 7788 21", account_name: "Laras Ayu Pramesti" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2650 7788", account_name: "Bayu Adi Nugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Slamet Riyadi No. 214, Laweyan, Kota Surakarta 57141" },
  ],
  guestName: "Bapak Hendro Wibowo & Keluarga",
  guestTable: "12",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin", note: "Diiringi gendhing Kebo Giro" },
      { time: "11.15", title: "Upacara panggih", note: "Balangan gantal, wiji dadi, sindur binayang" },
      { time: "12.00", title: "Resepsi & ramah tamah" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Nuansa marun, krem, dan emas. Batik atau kebaya dipersilakan.", colors: ["#6b1e24", "#f6ecdc", "#c29a4a", "#3f2312"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-19T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Drs. Sutrisno Hadi", "Kel. Besar Bpk. Agus Prasetyo", "Sanggar Karawitan Ngesti Laras"] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Tentu, putra-putri sangat diterima." },
      { q: "Apakah upacara panggih terbuka untuk tamu?", a: "Ya, seluruh tamu dapat menyaksikan upacara panggih sebelum resepsi." },
    ] },
  },
});
