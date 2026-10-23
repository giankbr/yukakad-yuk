import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahira", groom: "Rayhan",
    brideFull: "Zahira Nur Faiza, S.Hum.", groomFull: "Rayhan Akbar Maulana, S.E.",
    brideParents: "Putri pertama dari\nBapak H. Fauzan Alatas & Ibu Hj. Syarifah Nabila", groomParents: "Putra ketiga dari\nBapak H. Ahmad Sujatmiko & Ibu Hj. Rahmawati",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti kafilah yang menemukan tempat singgah di ujung perjalanan, kami menemukan rumah pada satu sama lain.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-11T08:00:00+07:00",
  place: "Balai Kartini",
  address: "Jl. Gatot Subroto Kav. 37, Kuningan Timur, Setiabudi, Jakarta Selatan",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Peta di Perpustakaan", body: "Kami sama-sama meminjam buku tentang Jalur Sutra di perpustakaan kampus. Hanya ada satu eksemplar, jadi kami membacanya bergantian." },
    { date: "2024", title: "Perjalanan ke Samarkand", body: "Dalam rombongan studi sejarah, kami berdiri di halaman sebuah karavanserai tua saat senja. Di sanalah kami mulai bicara tentang masa depan." },
    { date: "2026", title: "Khitbah", body: "Keluarga Rayhan datang meminang dengan doa dan restu. Kami sepakat melangkah bersama, insyaallah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sunda Kelapa", address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat" },
    { name: "Walimatul 'Ursy", date: "2027-09-11T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Kartini", address: "Jl. Gatot Subroto Kav. 37, Kuningan Timur, Setiabudi, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a131.webp", "/themes/img/a23.webp", "/themes/img/r84.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7209 4418 30", account_name: "Zahira Nur Faiza" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1240 0118 7342 5", account_name: "Rayhan Akbar Maulana" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Timur Raya No. 48, Bangka, Mampang Prapatan, Jakarta Selatan 12730" },
  ],
  guestName: "Bapak H. Salim Bahasuan & Keluarga",
  guestTable: "Meja Bukhara 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu", note: "Diiringi gambus dan marawis" },
      { time: "11.30", title: "Kirab kedua mempelai" },
      { time: "12.00", title: "Doa bersama & tausiyah singkat" },
      { time: "12.30", title: "Jamuan & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim formal bernuansa hangat: terakota, merah delima, biru nila, atau tembaga.", colors: ["#b5653a", "#8c2a22", "#26305a", "#b8693a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-11T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Fauzan Alatas", "Kel. Besar H. Ahmad Sujatmiko"] },
    faq: { items: [
      { q: "Apakah tersedia musala?", a: "Musala tersedia di lantai dasar Balai Kartini, lengkap dengan perlengkapan salat." },
      { q: "Apakah akad terbuka untuk tamu?", a: "Akad dihadiri keluarga inti. Tamu undangan dipersilakan hadir pada walimah pukul 11.00." },
    ] },
  },
});
