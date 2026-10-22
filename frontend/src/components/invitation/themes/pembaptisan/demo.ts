import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Mikha", groom: "",
    brideFull: "Mikhael Gabriel Wibisono",
    brideParents: "Putra pertama dari Bapak Yohanes Wibisono & Ibu Maria Clara Kusumawati",
    note: "Dengan sukacita kami membawa Mikha ke hadapan Tuhan untuk menerima Sakramen Pembaptisan Kudus.",
  },
  eventLabel: "Pembaptisan Kudus",
  date: "2027-03-07T09:00:00+07:00",
  place: "Gereja Santa Maria Penolong Abadi",
  address: "Jl. Kaliurang Km 6,5 No. 14, Condongcatur, Depok, Sleman, Yogyakarta",
  story: { title: "", body: "" },
  stories: [
    { date: "8 November 2026", title: "Anugerah pertama", body: "Mikha lahir di pagi yang hujan, membawa sukacita yang tak terkatakan bagi keluarga kecil kami." },
    { date: "Arti nama", title: "Mikhael Gabriel", body: "Mikhael berarti \"siapakah seperti Allah\", Gabriel berarti \"Allah adalah kekuatanku\". Doa kami terselip di namanya." },
    { date: "7 Maret 2027", title: "Langkah iman pertama", body: "Bersama orang tua dan wali baptisnya, Mikha diterima dalam persekutuan umat Allah." },
  ],
  events: [
    { name: "Misa & Sakramen Pembaptisan", date: "2027-03-07T09:00:00+07:00", time: "09.00 – 11.00 WIB", venue: "Gereja Santa Maria Penolong Abadi", address: "Jl. Kaliurang Km 6,5 No. 14, Condongcatur, Depok, Sleman, Yogyakarta" },
    { name: "Syukuran & Ramah Tamah", date: "2027-03-07T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "Kediaman Keluarga Wibisono", address: "Jl. Palagan Tentara Pelajar No. 33, Sariharjo, Ngaglik, Sleman, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0373 6612 84", account_name: "Maria Clara Kusumawati" },
  ],
  guestName: "Keluarga Bapak Antonius Setiawan",
  guestTable: "",
  extras: {
    quote: { text: "Biarkanlah anak-anak itu datang kepada-Ku, jangan menghalang-halangi mereka, sebab orang-orang yang seperti itulah yang empunya Kerajaan Allah.", source: "Markus 10:14" },
    child: { name: "Mikhael Gabriel Wibisono", nickname: "Mikha", birthDate: "2026-11-08T06:20:00+07:00", parents: "Putra pertama dari Bapak Yohanes Wibisono & Ibu Maria Clara Kusumawati" },
    rundown: { items: [
      { time: "09.00", title: "Misa Kudus", note: "Mohon hadir 15 menit lebih awal" },
      { time: "10.15", title: "Ritus Pembaptisan", note: "Bersama orang tua & wali baptis" },
      { time: "10.45", title: "Foto bersama keluarga" },
      { time: "11.30", title: "Syukuran & ramah tamah di rumah" },
    ] },
    dressCode: { note: "Busana sopan bernuansa putih atau warna lembut.", colors: ["#ffffff", "#f3ecdf", "#cfe3ec", "#c9d3c0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Wali Baptis & Keluarga", names: ["Bapak Stefanus Hartanto (Wali Baptis)", "Ibu Agnes Lestari (Wali Baptis)", "Opa & Oma Wibisono", "Kakek & Nenek Kusumawati"] },
    faq: { items: [
      { q: "Apakah tamu non-Katolik boleh hadir di Misa?", a: "Tentu, semua tamu dipersilakan hadir dan ikut mendoakan Mikha." },
      { q: "Di mana parkir kendaraan?", a: "Halaman gereja dan lapangan SD di sebelah barat gereja." },
    ] },
  },
});
