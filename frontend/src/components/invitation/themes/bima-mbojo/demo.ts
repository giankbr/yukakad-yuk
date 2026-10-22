import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nurul", groom: "Ikhsan",
    brideFull: "Nurul Hidayati, S.Kep.", groomFull: "Muhammad Ikhsan Ramdhani, S.H.",
    brideParents: "Putri ketiga dari\nBapak H. Abdul Gani M. Saleh & Ibu Hj. Siti Aminah", groomParents: "Putra kedua dari\nBapak Drs. Syamsuddin Ahmad & Ibu Hadijah",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti padi yang disimpan rapi di uma lengge, semoga setiap kebaikan kami tersimpan untuk musim-musim yang akan datang.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-26T09:00:00+08:00",
  place: "Masjid Sultan Muhammad Salahuddin",
  address: "Jl. Sultan Kaharuddin, Paruga, Rasanae Barat, Kota Bima, Nusa Tenggara Barat",
  stories: [
    { date: "2019", title: "Sore di Pantai Lawata", body: "Kami bertemu di kegiatan bakti sosial kampus. Senja di Teluk Bima menjadi saksi obrolan panjang pertama kami." },
    { date: "2025", title: "Lamaran", body: "Keluarga Ikhsan datang melamar dengan penuh hormat. Dua keluarga bermusyawarah dan menetapkan hari baik." },
    { date: "2027", title: "Akad Nikah", body: "Dengan memohon rida Allah, kami berjanji di hadapan keluarga dan saksi, di masjid kebanggaan Dana Mbojo." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-26T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Sultan Muhammad Salahuddin", address: "Jl. Sultan Kaharuddin, Paruga, Rasanae Barat, Kota Bima" },
    { name: "Walimatul 'Ursy", date: "2027-06-26T19:30:00+08:00", time: "19.30 – 22.00 WITA", venue: "Gedung Paruga Nae", address: "Jl. Gajah Mada, Monggonao, Mpunda, Kota Bima" },
  ],
  gallery: ["/themes/img/r81.webp", "/themes/img/r103.webp", "/themes/img/r76.webp", "/themes/img/r89.webp", "/themes/img/r13.webp"],
  gifts: [
    { id: "demo-ntbs", type: "bank", bank_name: "Bank NTB Syariah", account_number: "0060 1023 4471 8", account_name: "Nurul Hidayati" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 0423 59", account_name: "Muhammad Ikhsan Ramdhani" },
  ],
  guestName: "Bapak H. Ishaka Abubakar & Keluarga",
  guestTable: "Meja Lengge 2",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "19.30", title: "Penyambutan tamu", note: "Diiringi gambo dan biola Mbojo" },
      { time: "20.00", title: "Doa & sambutan keluarga" },
      { time: "20.30", title: "Ramah tamah", note: "Uta mbeca dan sepi tumis" },
      { time: "21.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim resmi. Tembe dan rimpu dipersilakan; merah, ungu, dan kuning kunyit.", colors: ["#8e1f3a", "#2c1830", "#d9a03a", "#f7ecdc"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-26T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Gani M. Saleh", "Kel. Besar Drs. Syamsuddin Ahmad"] },
  },
});
