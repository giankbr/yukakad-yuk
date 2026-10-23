import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sarifa", groom: "Fadli",
    brideFull: "Sarifa Ayu Hi. Abdullah, S.Kep.", groomFull: "Muhammad Fadli Ismail, S.Pd.",
    brideParents: "Putri kedua dari\nBapak Hi. Abdullah Kader & Ibu Hj. Nursia Djafar", groomParents: "Putra sulung dari\nBapak Ismail Hi. Yusuf & Ibu Fatma Lamaradji",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti cengkih dan pala yang tumbuh di lereng Kie Matubu, kami ingin saling menjaga harum satu sama lain.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T09:00:00+09:00",
  place: "Masjid Sigi Kolano",
  address: "Kelurahan Soasio, Tidore, Kota Tidore Kepulauan, Maluku Utara",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Festival Hari Jadi Tidore", body: "Kami bertemu sebagai panitia lomba perahu di pantai Soasio. Sarifa mencatat nilai, Fadli yang paling sering salah hitung." },
    { date: "2025", title: "Antar Tanda", body: "Keluarga Fadli datang ke rumah membawa tanda ikatan. Di beranda yang menghadap laut, kedua keluarga bersepakat." },
    { date: "2027", title: "Akad Nikah", body: "Dengan memohon rida Allah, kami melangkah bersama di Masjid Sigi Kolano, di bawah bayang Kadato Kie." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T09:00:00+09:00", time: "09.00 – 10.30 WIT", venue: "Masjid Sigi Kolano", address: "Kelurahan Soasio, Tidore, Kota Tidore Kepulauan, Maluku Utara" },
    { name: "Walimatul 'Ursy", date: "2027-08-14T19:30:00+09:00", time: "19.30 – 22.00 WIT", venue: "Gedung Serbaguna Soasio", address: "Jl. Sultan Nuku No. 8, Soasio, Tidore, Kota Tidore Kepulauan" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r105.webp", "/themes/img/a21.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7183 2260 45", account_name: "Sarifa Ayu" },
    { id: "demo-malut", type: "bank", bank_name: "Bank Malut", account_number: "003 02 11 05518 2", account_name: "Muhammad Fadli Ismail" },
  ],
  guestName: "Bapak Hi. Rahman Sangaji & Keluarga",
  guestTable: "Meja Cengkih 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.30", title: "Penyambutan tamu", note: "Diiringi tari Kapita dan tifa" },
      { time: "20.00", title: "Doa & sambutan keluarga" },
      { time: "20.30", title: "Ramah tamah", note: "Ikan kuah kuning dan papeda" },
      { time: "21.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim resmi. Merah cengkih, hijau laut, dan krem dipersilakan.", colors: ["#7a2f26", "#24585c", "#f6ead8", "#c08a3e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Hi. Abdullah Kader", "Kel. Besar Ismail Hi. Yusuf", "Keluarga Soa Tomalou"] },
    faq: { items: [
      { q: "Bagaimana menuju Tidore dari Ternate?", a: "Naik speedboat dari Pelabuhan Bastiong ke Rum sekitar 10 menit, lalu lanjut ke Soasio sekitar 30 menit." },
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir di halaman gedung dan sepanjang Jl. Sultan Nuku." },
    ] },
  },
});
