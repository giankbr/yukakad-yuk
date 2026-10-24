import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Maryam", groom: "Ihsan",
    brideFull: "Maryam Nur Azizah, S.Farm.", groomFull: "Muhammad Ihsan Fadhlurrahman, Lc.",
    brideParents: "Putri pertama dari\nBapak H. Abdul Hakim & Ibu Hj. Siti Rahmah", groomParents: "Putra ketiga dari\nBapak Drs. H. Ahmad Syarifuddin & Ibu Hj. Nurlaila",
    note: "Seperti lili yang tumbuh lurus menuju cahaya, semoga langkah kami selalu tertuju kepada ridha-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-09T08:00:00+07:00",
  place: "Masjid Raya Bintaro Jaya",
  address: "Jl. Bintaro Utama 3A, Pondok Karya, Pondok Aren, Kota Tangerang Selatan",
  stories: [
    { date: "Rajab 1448 H", title: "Ta'aruf", body: "Dipertemukan melalui guru ngaji kedua keluarga. Kami bertukar biodata dan bertemu dengan didampingi wali." },
    { date: "Ramadhan 1448 H", title: "Khitbah", body: "Keluarga Ihsan datang ke rumah dengan niat baik. Lamaran diterima dengan penuh syukur." },
    { date: "Jumadil Awal 1449 H", title: "Akad & Walimah", body: "Insyaallah kami menyempurnakan separuh agama, memohon doa agar menjadi keluarga sakinah, mawaddah, warahmah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bintaro Jaya", address: "Jl. Bintaro Utama 3A, Pondok Karya, Pondok Aren, Kota Tangerang Selatan" },
    { name: "Walimatul 'Ursy", date: "2027-10-09T10:30:00+07:00", time: "10.30 – 13.00 WIB", venue: "Aula Serbaguna Masjid Raya Bintaro Jaya", address: "Jl. Bintaro Utama 3A, Pondok Karya, Pondok Aren, Kota Tangerang Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2286 51", account_name: "Maryam Nur Azizah" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3310 0459 72", account_name: "Muhammad Ihsan Fadhlurrahman" },
    { id: "demo-kado", type: "address", address: "Jl. Kasuari IX Blok HB 5 No. 12, Sektor 9, Bintaro Jaya, Tangerang Selatan 15229" },
  ],
  guestName: "Ustadzah Fatimah Az-Zahra & Keluarga",
  guestTable: "Meja Lili 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "10.30", title: "Kedatangan tamu", note: "Tempat duduk tamu pria dan wanita terpisah" },
      { time: "11.00", title: "Tilawah & tausiyah walimah" },
      { time: "11.45", title: "Doa bersama untuk kedua mempelai" },
      { time: "12.15", title: "Ramah tamah", note: "Hidangan disajikan per meja" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Nuansa putih gading, hijau daun, dan emas lembut.", colors: ["#fffcf4", "#e9e1cc", "#4f6e55", "#b8914a"] },
    guestPass: {},
    family: { names: ["Kel. Besar H. Abdul Hakim (Bintaro)", "Kel. Besar Drs. H. Ahmad Syarifuddin (Bogor)"] },
  },
});
