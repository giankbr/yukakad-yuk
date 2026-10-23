import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Rizky",
    brideFull: "Nur Aisyah Rahmadani, S.Pd.", groomFull: "Muhammad Rizky Fadillah, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Zulkarnain & Ibu Hj. Rosmawati",
    groomParents: "Putra sulung dari\nBapak Abdul Hamid & Ibu Siti Mardiana",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti benang emas yang ditenun sehelai demi sehelai pada kain cual, kami ingin merajut hari-hari bersama dengan sabar.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-19T08:00:00+07:00",
  place: "Gedung Mahligai Cempaka",
  address: "Jl. Jenderal Sudirman No. 88, Gabek, Pangkalpinang, Kepulauan Bangka Belitung",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Bertemu di Mentok", body: "Kami pertama kali bertemu saat menjadi panitia festival budaya di Mentok. Rizky mengurus panggung, Aisyah mengajar tari Campak untuk anak-anak." },
    { date: "2024", title: "Menenun Kesabaran", body: "Tiga tahun berjarak, Pangkalpinang dan Palembang. Kami belajar bahwa kain yang indah selalu ditenun pelan-pelan." },
    { date: "2026", title: "Lamaran", body: "Keluarga Rizky datang membawa tepak sirih dan selembar kain cual merah. Kedua keluarga sepakat, bismillah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Jamik Pangkalpinang", address: "Jl. Masjid Jamik, Kel. Masjid Jamik, Rangkui, Pangkalpinang" },
    { name: "Resepsi & Nganggung", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung Mahligai Cempaka", address: "Jl. Jenderal Sudirman No. 88, Gabek, Pangkalpinang, Kepulauan Bangka Belitung" },
  ],
  gallery: ["/themes/img/a21.webp", "/themes/img/r6.webp", "/themes/img/a22.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 4488 19", account_name: "Nur Aisyah Rahmadani" },
    { id: "demo-sumselbabel", type: "bank", bank_name: "Sumsel Babel", account_number: "160 09 31772", account_name: "Muhammad Rizky Fadillah" },
    { id: "demo-alamat", type: "address", address: "Jl. Mentok No. 21, Bukit Merapin, Gerunggang, Pangkalpinang 33123" },
  ],
  guestName: "Bapak Datuk Ismail & Keluarga",
  guestTable: "Cempaka 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Arak-arakan pengantin", note: "Diiringi rebana dan tari Campak" },
      { time: "11.00", title: "Resepsi dibuka", note: "Tepung tawar & doa" },
      { time: "12.00", title: "Nganggung", note: "Makan bersama dari dulang" },
    ] },
    dressCode: { note: "Baju kurung, teluk belanga, atau batik. Kain cual sangat dipersilakan.", colors: ["#a22f38", "#d8b25c", "#efb9ae", "#3c9fa4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkarnain (Pangkalpinang)", "Kel. Besar Abdul Hamid (Mentok)", "Keluarga Besar Datuk Usman", "Sanggar Tari Serumpun Sebalai"] },
    travel: { note: "Untuk tamu dari luar pulau, berikut beberapa pilihan terdekat.", items: [
      { name: "Bandara Depati Amir", detail: "± 15 menit ke gedung resepsi" },
      { name: "Penginapan keluarga", detail: "Hubungi panitia untuk kamar di sekitar Jl. Sudirman" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh membawa dulang nganggung?", a: "Boleh sekali. Panitia juga menyiapkan dulang bagi tamu dari luar daerah." },
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir di halaman gedung dan di sepanjang Jl. Sudirman." },
    ] },
  },
});
