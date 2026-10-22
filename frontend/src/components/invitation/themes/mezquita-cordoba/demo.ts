import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Rayyan",
    brideFull: "Aisyah Zahra Firdausi, S.Ars.", groomFull: "Muhammad Rayyan Hakim, M.T.",
    brideParents: "Putri pertama dari\nBapak Dr. H. Fauzan Firdausi & Ibu Hj. Laila Rahmawati", groomParents: "Putra ketiga dari\nBapak H. Abdul Hakim Lubis & Ibu Hj. Siti Mariam",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Seperti deretan lengkung yang saling menopang, kami ingin membangun rumah tangga yang kokoh: saling menguatkan, dan selalu menghadap ke arah yang sama.",
  },
  eventLabel: "Walimatul 'Urs",
  date: "2027-05-15T08:00:00+07:00",
  place: "Gedung Puri Andalus, Bandung",
  address: "Jl. Dr. Setiabudi No. 188, Hegarmanah, Cidadap, Kota Bandung",
  stories: [
    { date: "2018", title: "Studio Arsitektur", body: "Kami bertemu di studio kampus. Aisyah menggambar lengkung tapal kuda untuk tugas akhir, Rayyan menghitung strukturnya." },
    { date: "2022", title: "Lengkung yang Sama", body: "Perjalanan studi ke masjid-masjid tua mengajarkan kami bahwa keindahan lahir dari kesabaran dan ketelitian." },
    { date: "2026", title: "Khitbah", body: "Dengan niat baik, keluarga Rayyan datang mengkhitbah. Alhamdulillah, kedua keluarga merestui." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Irsyad", address: "Kota Baru Parahyangan, Padalarang, Kabupaten Bandung Barat" },
    { name: "Walimah", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Puri Andalus", address: "Jl. Dr. Setiabudi No. 188, Hegarmanah, Cidadap, Kota Bandung" },
  ],
  gallery: ["/themes/img/a49.webp", "/themes/img/a43.webp", "/themes/img/r75.webp", "/themes/img/r57.webp", "/themes/img/r26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7150 3366 21", account_name: "Aisyah Zahra Firdausi" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 8812 09", account_name: "Muhammad Rayyan Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Cipaganti No. 61, Coblong, Kota Bandung 40131" },
  ],
  guestName: "Bapak H. Syamsul Arifin & Keluarga",
  guestTable: "Meja Qurtubah 4",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Kedatangan kedua mempelai" },
      { time: "11.15", title: "Tilawah & tausiyah singkat" },
      { time: "11.45", title: "Doa bersama & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim yang sopan. Nuansa bata, gading, dan keemasan dipersilakan.", colors: ["#a8432c", "#ecdcbc", "#d9a441", "#3a2416"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-15T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Dr. H. Fauzan Firdausi (Bandung)", "Kel. Besar H. Abdul Hakim Lubis (Medan)"] },
  },
});
