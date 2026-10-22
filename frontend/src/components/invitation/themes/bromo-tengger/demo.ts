import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahayu", groom: "Wahyu",
    brideFull: "Sri Rahayu Kartikasari, S.Pd.", groomFull: "Wahyu Adi Pranata",
    brideParents: "Putri kedua dari\nBapak Sukarman & Ibu Ngatini", groomParents: "Putra sulung dari\nBapak Karyono & Ibu Supiyati",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Seperti kabut yang setia memeluk lautan pasir setiap fajar, kami berjanji saling menjaga di setiap musim.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Balai Desa Ngadisari",
  address: "Jl. Raya Bromo, Desa Ngadisari, Kec. Sukapura, Kabupaten Probolinggo, Jawa Timur",
  stories: [
    { date: "2019", title: "Bertemu di Kasada", body: "Rahayu dan Wahyu sama-sama membantu keluarga menyiapkan ongkek untuk Yadnya Kasada. Di tengah dingin malam lautan pasir, obrolan pertama dimulai." },
    { date: "2023", title: "Fajar di Penanjakan", body: "Wahyu yang setiap hari mengantar tamu melihat matahari terbit, akhirnya mengajak Rahayu sendiri ke Penanjakan dan menyampaikan niat baiknya." },
    { date: "2027", title: "Walagara", body: "Dengan restu kedua orang tua dan doa romo dukun pandita, kami melangkah ke upacara walagara di desa kelahiran kami." },
  ],
  events: [
    { name: "Upacara Walagara", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 11.00 WIB", venue: "Kediaman Mempelai Putri", address: "Dusun Ngadisari RT 02 RW 01, Desa Ngadisari, Kec. Sukapura, Probolinggo" },
    { name: "Resepsi & Syukuran", date: "2027-07-10T13:00:00+07:00", time: "13.00 – 17.00 WIB", venue: "Balai Desa Ngadisari", address: "Jl. Raya Bromo, Desa Ngadisari, Kec. Sukapura, Kabupaten Probolinggo" },
  ],
  gallery: ["/themes/img/r102.webp", "/themes/img/r104.webp", "/themes/img/a30.webp", "/themes/img/r89.webp", "/themes/img/r14.webp", "/themes/img/r61.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Jatim", account_number: "0312 4471 908", account_name: "Sri Rahayu Kartikasari" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "6170 0102 3345 508", account_name: "Wahyu Adi Pranata" },
    { id: "demo-kado", type: "address", address: "Dusun Ngadisari RT 02 RW 01, Desa Ngadisari, Kec. Sukapura, Probolinggo 67254" },
  ],
  guestName: "Bapak Sugiyanto & Keluarga",
  guestTable: "Meja Penanjakan",
  extras: {
    quote: { text: "Wahai pasangan suami istri, semoga kalian tetap bersatu dan tidak pernah terpisahkan. Semoga kalian mencapai hidup yang penuh kebahagiaan bersama keturunan, dalam rumah yang penuh suka cita.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "13.00", title: "Penyambutan tamu", note: "Gamelan & tari Tengger" },
      { time: "13.45", title: "Doa syukur bersama" },
      { time: "14.30", title: "Makan bersama", note: "Nasi jagung, sayur kentang & sambal tomat" },
      { time: "16.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Udara Ngadisari dingin (12–16°C). Busana hangat bernuansa bumi; sarung atau syal sangat dianjurkan.", colors: ["#7e2f2a", "#d8b56a", "#5d7a44", "#efe2c4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Sukarman", "Kel. Besar Bpk. Karyono", "Warga Desa Ngadisari"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan menginap di Sukapura.", items: [
      { name: "Homestay warga Ngadisari", detail: "± 300 m dari balai desa, bisa dipesan lewat keluarga" },
      { name: "Jalur dari Probolinggo", detail: "± 1,5 jam berkendara, siapkan jaket karena berkabut sore hari" },
    ] },
  },
});
