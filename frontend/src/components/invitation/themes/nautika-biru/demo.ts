import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ines", groom: "Arka",
    brideFull: "Ines Maharani Tanjung, S.T.", groomFull: "Arka Wiradharma, S.Pi.",
    brideParents: "Putri ketiga dari\nBapak Rudy Tanjung & Ibu Sri Rahayu", groomParents: "Putra kedua dari\nBapak Kapten (Purn.) Dharma Wijaya & Ibu Lenny Kartika",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Dua kompas yang akhirnya menunjuk ke arah yang sama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T15:30:00+07:00",
  place: "Paviliun Dermaga Lama",
  address: "Jl. Pelabuhan Tua No. 3, Penjaringan, Jakarta Utara",
  story: { title: "Catatan Pelayaran", body: "" },
  stories: [
    { date: "Juli 2020", title: "Satu Kapal Feri", body: "Penyeberangan Merak menuju Bakauheni. Ines kehilangan topinya ditiup angin, Arka yang menangkapnya di geladak." },
    { date: "2022", title: "Belajar Berlayar", body: "Setiap Minggu pagi kami ikut kelas layar di Teluk Jakarta. Ines selalu jadi nakhoda, Arka setia memegang tali." },
    { date: "Februari 2027", title: "Di Ujung Dermaga", body: "Saat matahari terbenam, Arka berlutut di ujung dermaga dengan cincin yang diikat simpul tali kecil." },
  ],
  events: [
    { name: "Pemberkatan & Janji Suci", date: "2027-08-21T15:30:00+07:00", time: "15.30 – 16.30 WIB", venue: "Geladak Paviliun Dermaga Lama", address: "Jl. Pelabuhan Tua No. 3, Penjaringan, Jakarta Utara" },
    { name: "Resepsi Senja", date: "2027-08-21T18:00:00+07:00", time: "18.00 – 21.00 WIB", venue: "Paviliun Dermaga Lama", address: "Jl. Pelabuhan Tua No. 3, Penjaringan, Jakarta Utara" },
  ],
  gallery: ["/themes/img/r15.webp", "/themes/img/r11.webp", "/themes/img/r103.webp", "/themes/img/r9.webp", "/themes/img/r10.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "126 00 0981 2207", account_name: "Ines Maharani Tanjung" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0811 9020 3341", account_name: "Arka Wiradharma" },
  ],
  guestName: "Bapak Hendra Simatupang & Keluarga",
  guestTable: "Meja Jangkar 7",
  extras: {
    quote: { text: "Kapal di pelabuhan memang aman, tetapi bukan untuk itu kapal dibuat.", source: "John A. Shedd" },
    rundown: { items: [
      { time: "15.30", title: "Pemberkatan di geladak", note: "Keluarga inti & sahabat" },
      { time: "16.30", title: "Lempar bunga ke laut" },
      { time: "18.00", title: "Resepsi senja dibuka" },
      { time: "19.30", title: "Dansa pertama & potong kue" },
    ] },
    dressCode: { note: "Navy, putih, dan sentuhan merah. Garis-garis sangat dipersilakan.", colors: ["#1b2a4a", "#f5f2ea", "#c23b2e", "#b8893a"] },
    guestPass: {},
    rsvpDietary: {},
    travel: { note: "Lokasi dekat kawasan kota tua. Beberapa pilihan menuju dermaga:", items: [
      { name: "Stasiun Jakarta Kota", detail: "± 10 menit berkendara" },
      { name: "Parkir & shuttle", detail: "Parkir di gerbang barat, shuttle tiap 15 menit" },
    ] },
  },
});
