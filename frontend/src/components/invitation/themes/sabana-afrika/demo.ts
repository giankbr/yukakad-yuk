import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Damar",
    brideFull: "Sekar Ayuningtyas, S.Hut.", groomFull: "Damar Prakoso Nugroho, S.T.",
    brideParents: "Putri kedua dari\nBapak Haryo Wicaksono & Ibu Retno Palupi", groomParents: "Putra sulung dari\nBapak Antonius Nugroho & Ibu Maria Kristiani",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti padang rumput yang menunggu senja, kami belajar bahwa hal terindah datang pada waktunya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T16:00:00+07:00",
  place: "Padang Savana Lodge",
  address: "Jl. Raya Waingapu – Melolo Km 22, Kambera, Sumba Timur, Nusa Tenggara Timur",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Africa van Java", body: "Kami bertemu dalam rombongan pengamat burung di Savana Bekol, Baluran. Sekar sibuk mencatat merak hijau, Damar sibuk memotret matahari terbenam." },
    { date: "2024", title: "Bukit-Bukit Sumba", body: "Perjalanan berdua ke padang Wairinding. Di antara rumput emas dan kuda-kuda liar, Damar memberanikan diri melamar." },
    { date: "2027", title: "Senja yang Kami Pilih", body: "Kami mengikat janji di bawah langit jingga Sumba Timur, ditemani keluarga dan sahabat terdekat." },
  ],
  events: [
    { name: "Pemberkatan & Janji Nikah", date: "2027-07-17T16:00:00+07:00", time: "16.00 – 17.00 WITA", venue: "Bukit Akasia, Padang Savana Lodge", address: "Jl. Raya Waingapu – Melolo Km 22, Kambera, Sumba Timur" },
    { name: "Resepsi Senja", date: "2027-07-17T17:30:00+07:00", time: "17.30 – 21.00 WITA", venue: "Padang Savana Lodge", address: "Jl. Raya Waingapu – Melolo Km 22, Kambera, Sumba Timur" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/r109.webp", "/themes/img/r107.webp", "/themes/img/r108.webp", "/themes/img/r106.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1440 0127 3391", account_name: "Sekar Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Jl. Kaliurang Km 7, Perum Griya Asri B-4, Sleman, Yogyakarta 55581" },
  ],
  guestName: "Bapak Yohanes Umbu & Keluarga",
  guestTable: "Akasia 3",
  extras: {
    quote: { text: "Cinta tidak saling memandang satu sama lain, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "16.00", title: "Janji nikah di Bukit Akasia", note: "Tamu dimohon hadir 15 menit lebih awal" },
      { time: "17.15", title: "Foto bersama saat golden hour" },
      { time: "17.30", title: "Resepsi senja & makan malam" },
      { time: "19.30", title: "Api unggun & musik akustik" },
    ] },
    dressCode: { note: "Warna tanah dan senja: terakota, mustard, krem, dan cokelat. Sepatu datar sangat disarankan karena acara di atas rumput.", colors: ["#bb4329", "#f0a43e", "#561d33", "#e9d6b4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-17T16:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Haryo Wicaksono", "Kel. Besar Bpk. Antonius Nugroho"] },
    travel: { note: "Lokasi sekitar 40 menit dari Bandara Umbu Mehang Kunda, Waingapu.", items: [
      { name: "Shuttle tamu", detail: "Berangkat dari bandara pukul 13.00 dan 14.00 WITA" },
      { name: "Penginapan", detail: "Kamar di Padang Savana Lodge tersedia dengan kode SEKARDAMAR" },
    ] },
  },
});
