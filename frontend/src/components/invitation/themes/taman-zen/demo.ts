import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anindya", groom: "Bagas",
    brideFull: "Anindya Kusumaningtyas", groomFull: "Bagas Prasetyo Wicaksono",
    brideParents: "Putri dari\nBapak Hendra Kusuma & Ibu Ratna Widyaningsih",
    groomParents: "Putra dari\nBapak Agus Wicaksono & Ibu Lestari Handayani",
    bridePhoto: "/themes/img/r91.webp",
    groomPhoto: "/themes/img/r90.webp",
    note: "Seperti garis-garis pasir yang dirapikan setiap pagi, kami memilih untuk merawat hal-hal kecil, pelan dan setiap hari.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T15:00:00+07:00",
  place: "Taman Batu Saung Rasa",
  address: "Jl. Kolonel Masturi No. 88, Cikole, Lembang, Kabupaten Bandung Barat",
  stories: [
    { date: "2022", title: "Satu Meja di Kelas Keramik", body: "Tangan kami sama-sama penuh tanah liat. Mangkuk pertama Bagas retak, Anindya tertawa, lalu kami pulang bersama." },
    { date: "2024", title: "Musim Hujan di Kyoto", body: "Perjalanan kantor yang kebetulan sama. Kami menghabiskan sore di sebuah taman batu, diam, dan merasa cukup." },
    { date: "Januari 2027", title: "Sebuah Batu Kecil", body: "Bagas melamar dengan cincin yang diletakkan di atas batu sungai yang ia pungut sendiri. Jawabannya: iya." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-05-15T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Taman Batu Saung Rasa", address: "Jl. Kolonel Masturi No. 88, Cikole, Lembang, Kabupaten Bandung Barat" },
    { name: "Jamuan Senja", date: "2027-05-15T16:30:00+07:00", time: "16.30 – 19.30 WIB", venue: "Paviliun Kayu Saung Rasa", address: "Jl. Kolonel Masturi No. 88, Cikole, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/r88.webp", "/themes/img/r13.webp", "/themes/img/r55.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "4370 2281 96", account_name: "Anindya Kusumaningtyas" },
    { id: "demo-wallet", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2214 7783", account_name: "Bagas Prasetyo W." },
  ],
  guestName: "Ibu Sekar Arumdalu",
  guestTable: "Meja Batu 4",
  extras: {
    quote: { text: "Cinta bukanlah saling memandang, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "15.00", title: "Upacara pernikahan", note: "Di taman batu, tamu duduk di bangku kayu" },
      { time: "16.00", title: "Teh & ucapan selamat" },
      { time: "16.30", title: "Jamuan senja", note: "Hidangan Nusantara & Jepang" },
      { time: "19.00", title: "Penutup" },
    ] },
    dressCode: { note: "Warna tanah dan batu: pasir, abu, hijau lumut. Sepatu datar sangat disarankan karena area berpasir.", colors: ["#e8e1d2", "#8d8980", "#7d8a4c", "#2f2d2a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Keluarga Bapak Hendra Kusuma", "Keluarga Bapak Agus Wicaksono"] },
    faq: { items: [
      { q: "Apakah acaranya di luar ruangan?", a: "Upacara di taman terbuka. Bila hujan, seluruh acara pindah ke paviliun kayu di sebelahnya." },
      { q: "Apakah tersedia parkir?", a: "Parkir tersedia di area depan Saung Rasa, lalu berjalan kaki sekitar dua menit." },
    ] },
  },
});
