import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "",
    brideFull: "Aisyah Nur Rahmania",
    brideParents: "Putri pertama dari Bapak Fauzan Hakim & Ibu Laila Rahmawati",
    note: "Alhamdulillah, setelah empat tahun belajar mengaji dengan sabar, Aisyah telah menyelesaikan bacaan Al-Qur'an 30 juz.",
  },
  eventLabel: "Khataman Al-Qur'an",
  date: "2027-05-23T08:00:00+07:00",
  place: "Masjid Al-Ikhlas Griya Asri",
  address: "Jl. Cempaka Raya No. 2, Griya Asri, Sukmajaya, Kota Depok",
  story: { title: "Perjalanan Mengaji", body: "" },
  stories: [
    { date: "2022", title: "Iqra' pertama", body: "Di usia lima tahun Aisyah mulai belajar huruf hijaiyah di TPA Al-Ikhlas, setiap sore selepas Asar." },
    { date: "2024", title: "Naik ke Al-Qur'an", body: "Selesai Iqra' 6 dan mulai membaca mushaf bersama Ustazah Maryam, satu halaman setiap hari." },
    { date: "2026", title: "Separuh perjalanan", body: "Sampai di juz 15 pada bulan Ramadan, ditemani Ayah yang menyimak bacaannya setiap malam." },
    { date: "2027", title: "Khatam 30 juz", body: "Alhamdulillah, ayat terakhir surat An-Nas dibaca dengan tartil di hadapan guru dan keluarga." },
  ],
  events: [
    { name: "Khataman & Doa Khatmil Qur'an", date: "2027-05-23T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Al-Ikhlas Griya Asri", address: "Jl. Cempaka Raya No. 2, Griya Asri, Sukmajaya, Kota Depok" },
    { name: "Tasyakuran & Ramah Tamah", date: "2027-05-23T10:30:00+07:00", time: "10.30 – 13.00 WIB", venue: "Kediaman Bapak Fauzan Hakim", address: "Jl. Flamboyan Blok C3 No. 14, Griya Asri, Sukmajaya, Kota Depok" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7123 4560 89", account_name: "Laila Rahmawati" },
  ],
  guestName: "Bapak H. Ridwan & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan sungguh, telah Kami mudahkan Al-Qur'an untuk peringatan, maka adakah orang yang mau mengambil pelajaran?", source: "QS. Al-Qamar: 17" },
    child: { name: "Aisyah Nur Rahmania", nickname: "Aisyah", birthDate: "2018-03-14T05:40:00+07:00", parents: "Putri pertama dari Bapak Fauzan Hakim & Ibu Laila Rahmawati" },
    rundown: { items: [
      { time: "08.00", title: "Pembukaan & tilawah", note: "Dipandu Ustazah Maryam" },
      { time: "08.20", title: "Aisyah membaca surat-surat pendek juz 30" },
      { time: "09.00", title: "Doa khatmil Qur'an bersama" },
      { time: "09.30", title: "Tausiyah singkat", note: "Ustaz Abdul Karim" },
      { time: "10.30", title: "Tasyakuran di rumah" },
    ] },
    dressCode: { note: "Busana muslim yang nyaman, nuansa hijau lembut dan krem.", colors: ["#24574a", "#8aa58a", "#f5efe1", "#c9a45a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Kakek & Nenek H. Abdul Hakim", "Kakek & Nenek Rahmat Hidayat", "Ustazah Maryam & keluarga TPA Al-Ikhlas"] },
    faq: { items: [
      { q: "Apakah anak-anak boleh ikut?", a: "Sangat boleh. Teman-teman mengaji Aisyah juga kami undang." },
      { q: "Di mana tempat untuk jamaah perempuan?", a: "Ruang utama sebelah kanan, dengan tabir. Mukena tersedia di masjid." },
    ] },
  },
});
