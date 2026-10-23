import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Fadhil",
    brideFull: "Salma Khairunnisa, S.Ars.", groomFull: "Fadhil Ahmad Rasyid, M.Hum.",
    brideParents: "Putri pertama dari\nBapak Drs. H. Ahmad Syarifuddin & Ibu Hj. Nurlaila",
    groomParents: "Putra ketiga dari\nBapak H. Rasyid Hamzah & Ibu Hj. Fauziah",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti kepingan kaca emas yang disusun satu per satu, kami ingin membangun rumah yang sabar, terang, dan saling menguatkan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-11T08:30:00+07:00",
  place: "Gedung Serbaguna Ar-Rahman",
  address: "Jl. Pemuda No. 17, Rawamangun, Pulo Gadung, Jakarta Timur",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Kelas Sejarah Arsitektur", body: "Salma meneliti ornamen masjid tua untuk tugas akhirnya, Fadhil menjadi asisten dosen yang terlalu banyak bertanya. Kami berdebat soal kubah dan pelengkung." },
    { date: "2023", title: "Perjalanan Studi", body: "Bersama rombongan kampus kami mengunjungi masjid-masjid bersejarah. Di sanalah Fadhil sadar ia ingin pulang dengan orang yang sama." },
    { date: "2026", title: "Khitbah", body: "Dengan restu kedua keluarga, Fadhil datang melamar. Kami memilih tanggal ini sambil menyusun mimpi kepingan demi kepingan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Agung Sunda Kelapa", address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat" },
    { name: "Walimah", date: "2027-09-11T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Ar-Rahman", address: "Jl. Pemuda No. 17, Rawamangun, Pulo Gadung, Jakarta Timur" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a123.webp", "/themes/img/a110.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7155 0203 61", account_name: "Salma Khairunnisa" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3410 0877 21", account_name: "Fadhil Ahmad Rasyid" },
    { id: "demo-alamat", type: "address", address: "Jl. Kayu Putih Raya No. 9, Pulo Gadung, Jakarta Timur 13260" },
  ],
  guestName: "Bapak H. Lukman Hakim & Keluarga",
  guestTable: "Dimasyq 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.30", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.30", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Pembacaan doa" },
      { time: "12.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim nuansa hijau zamrud, emas, atau gading.", colors: ["#1d4a36", "#d4b05a", "#f3ecd6", "#2f6f73"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar H. Rasyid Hamzah", "Keluarga Besar Bani Hamzah", "Rekan Program Studi Arsitektur"] },
    faq: { items: [
      { q: "Apakah tempat akad dan walimah berbeda?", a: "Ya. Akad di Masjid Agung Sunda Kelapa, walimah di Gedung Serbaguna Ar-Rahman, sekitar 30 menit berkendara." },
      { q: "Apakah tersedia area salat?", a: "Tersedia musala dan tempat wudu di lantai dasar gedung walimah." },
    ] },
  },
});
