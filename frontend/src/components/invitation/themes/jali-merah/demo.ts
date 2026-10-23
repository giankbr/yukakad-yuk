import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Faiz",
    brideFull: "Fatimah Az-Zahra Ramadhani, S.Ars.", groomFull: "Muhammad Faiz Hakim, M.T.",
    brideParents: "Putri pertama dari\nBapak H. Rizal Ramadhan & Ibu Hj. Nadia Lubis", groomParents: "Putra ketiga dari\nBapak H. Abdul Hakim & Ibu Hj. Salma Assegaf",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti cahaya yang menembus kisi-kisi batu, semoga kasih kami sederhana bentuknya namun terang bagi siapa saja di sekitar kami.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T08:00:00+07:00",
  place: "Masjid Nasional Al-Akbar Surabaya",
  address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya",
  stories: [
    { date: "2018", title: "Studio Arsitektur", body: "Kami satu kelompok tugas merancang ulang pasar lama. Zahra menggambar kisi-kisi fasad, Faiz menghitung bebannya." },
    { date: "2021", title: "Perjalanan Studi", body: "Rombongan kampus mengunjungi bangunan-bangunan bersejarah. Di bawah bayang kisi batu, Faiz memberanikan diri bertanya tentang masa depan." },
    { date: "2026", title: "Khitbah", body: "Keluarga Faiz datang bersilaturahmi ke rumah keluarga Zahra di Surabaya. Lamaran diterima dengan penuh syukur." },
    { date: "2027", title: "Akad Nikah", body: "Bismillah, kami menyempurnakan separuh agama di hadapan Allah dan keluarga tercinta." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Nasional Al-Akbar Surabaya", address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-10-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Grand City Convention Hall", address: "Jl. Walikota Mustajab No. 1, Ketabang, Genteng, Surabaya" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a139.webp", "/themes/img/a118.webp", "/themes/img/r57.webp", "/themes/img/a31.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 334 556", account_name: "Fatimah Az-Zahra Ramadhani" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "142 00 1188 776 5", account_name: "Muhammad Faiz Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Dharmahusada Indah Barat III No. 18, Mulyorejo, Surabaya 60115" },
  ],
  guestName: "Bapak H. Yusuf Alatas & Keluarga",
  guestTable: "Meja Diwan 4",
  extras: {
    quote: { text: "Allah (pemberi) cahaya (kepada) langit dan bumi. Perumpamaan cahaya-Nya seperti sebuah lubang yang tidak tembus, yang di dalamnya ada pelita besar.", source: "QS. An-Nur: 35" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin & doa" },
      { time: "11.30", title: "Sambutan keluarga" },
      { time: "12.00", title: "Jamuan makan siang" },
      { time: "13.00", title: "Foto bersama keluarga & sahabat" },
    ] },
    dressCode: { note: "Busana muslim formal. Terakota, krem, dan emas lembut dipersilakan.", colors: ["#9a4129", "#f1e6d2", "#c9a24e", "#4a1c10"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Rizal Ramadhan", "Kel. Besar H. Abdul Hakim"] },
  },
});
