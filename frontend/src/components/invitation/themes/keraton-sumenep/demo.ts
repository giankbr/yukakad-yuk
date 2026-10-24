import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Faiz",
    brideFull: "R. Ayu Nadia Rahmawati, S.Sn.", groomFull: "Moh. Faizur Rahman, S.H.",
    brideParents: "Putri bungsu dari\nBapak R. Ach. Mudhar & Ibu R. Ayu Siti Aminah", groomParents: "Putra kedua dari\nBapak H. Abd. Wahid & Ibu Hj. Rofiqoh",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Melewati Labang Mesem, gerbang yang menyambut setiap tamu dengan senyum, kami memulai rumah tangga dengan hati yang terbuka.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Pendopo Agung Keraton Sumenep",
  address: "Jl. Dr. Soetomo No. 6, Pajagalan, Kota Sumenep, Jawa Timur",
  stories: [
    { date: "2020", title: "Museum Keraton", body: "Nadia memandu rombongan mahasiswa hukum dari Surabaya di museum keraton. Faiz adalah satu-satunya yang terus bertanya soal kereta kencana." },
    { date: "2023", title: "Taman Sare", body: "Pertemuan berikutnya terjadi tak sengaja di Taman Sare saat festival budaya. Sejak itu kami rajin berkirim kabar." },
    { date: "2026", title: "Lamaran", body: "Keluarga Faiz datang melamar dengan membawa seserahan khas Madura. Dua keluarga sepakat menentukan hari baik." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jamik Panembahan Somala", address: "Jl. Trunojoyo No. 1, Bangselok, Kota Sumenep" },
    { name: "Resepsi", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Agung Keraton Sumenep", address: "Jl. Dr. Soetomo No. 6, Pajagalan, Kota Sumenep" },
  ],
  gallery: ["/themes/img/a46.webp", "/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a27.webp", "/themes/img/a62.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0251 8890 113", account_name: "R. Ayu Nadia Rahmawati" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2256 81", account_name: "Moh. Faizur Rahman" },
    { id: "demo-kado", type: "address", address: "Jl. Pahlawan Gg. II No. 14, Pajagalan, Kota Sumenep 69416" },
  ],
  guestName: "Bapak H. Moh. Ridwan & Keluarga",
  guestTable: "Pendopo 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin melewati Labang Mesem", note: "Diiringi musik saronen" },
      { time: "11.30", title: "Sambutan keluarga" },
      { time: "12.00", title: "Ramah tamah", note: "Soto Sumenep & kaldu kokot" },
      { time: "13.00", title: "Foto bersama di pendopo" },
    ] },
    dressCode: { note: "Busana muslim atau batik Madura. Warna cerah keraton sangat dipersilakan.", colors: ["#b5262b", "#e8b42a", "#2f7a52", "#f3ead8"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar R. Ach. Mudhar (Pajagalan)", "Kel. Besar H. Abd. Wahid (Kalianget)"] },
    travel: { note: "Untuk tamu dari luar Madura, berikut pilihan menginap di dekat keraton.", items: [
      { name: "Penginapan sekitar Jl. Trunojoyo", detail: "± 600 m dari keraton, jalan kaki ke Masjid Jamik" },
      { name: "Parkir tamu", detail: "Halaman Taman Bunga Sumenep, diantar becak ke pendopo" },
    ] },
  },
});
