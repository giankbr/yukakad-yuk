import { makeDemo } from "../demo-base";

// Betawi: palang pintu (rombongan pengantin pria dengan silat & pantun) → akad nikah → resepsi.
export const demo = makeDemo({
  couple: {
    bride: "Aini", groom: "Rizky",
    brideFull: "Nur Aini Maulida, S.Pd.", groomFull: "Muhammad Rizky Hidayatullah",
    brideParents: "Putri bungsu dari\nBapak H. Mamat Sarmili & Ibu Hj. Romlah", groomParents: "Putra kedua dari\nBapak H. Sanusi Napis & Ibu Hj. Mariyam",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T08:30:00+07:00",
  place: "Gedung Serbaguna Al-Hikmah",
  address: "Jl. Moh. Kahfi II No. 30, Srengseng Sawah, Jagakarsa, Jakarta Selatan",
  stories: [
    { date: "2020", title: "Kenal di Setu Babakan", body: "Aini bantu enyaknya jualan kerak telor tiap Minggu. Rizky pelanggan yang lama-lama dateng bukan cuma buat kerak telornya." },
    { date: "2023", title: "Ngedelengin", body: "Keluarga Rizky mulai main ke rumah, kenalan sama babe dan enyak Aini sambil ngopi sore." },
    { date: "2026", title: "Bawa Tande Putus", body: "Rombongan keluarga dateng ngelamar, bawa tande putus. Dua keluarga sepakat, tinggal nentuin hari baik." },
  ],
  events: [
    { name: "Palang Pintu & Akad Nikah", date: "2027-09-18T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Kediaman Mempelai Wanita", address: "Jl. Moh. Kahfi II Gg. Masjid No. 12, Srengseng Sawah, Jagakarsa, Jakarta Selatan" },
    { name: "Resepsi", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung Serbaguna Al-Hikmah", address: "Jl. Moh. Kahfi II No. 30, Srengseng Sawah, Jagakarsa, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a25.webp", "/themes/img/a31.webp", "/themes/img/r70.webp", "/themes/img/r63.webp", "/themes/img/a23.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0099 88", account_name: "Nur Aini Maulida" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0857 1122 3344", account_name: "M. Rizky Hidayatullah" },
  ],
  guestName: "Bapak H. Jaelani & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.30", title: "Palang pintu", note: "Silat, pantun & sike dari rombongan abang" },
      { time: "09.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "11.00", title: "Resepsi dibuka", note: "Diiringi gambang kromong" },
      { time: "13.00", title: "Arak-arakan ondel-ondel" },
    ] },
    dressCode: { note: "Bebas rapi, warna cerah. Kebaya kerancang atau baju sadariah boleh banget.", colors: ["#d1262f", "#157a4b", "#f4c430", "#fff5df"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T08:30:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Mamat Sarmili", "Kel. Besar H. Sanusi Napis", "Sanggar Silat Beksi Jagakarsa", "Warga RT 05 / RW 08 Srengseng Sawah"] },
    faq: { items: [
      { q: "Boleh bawa anak?", a: "Boleh banget, ajak aje sekeluarga." },
      { q: "Ada parkir?", a: "Ada parkir di halaman gedung dan lapangan sebelah masjid." },
    ] },
  },
});
