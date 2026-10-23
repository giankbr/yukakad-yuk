import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tara", groom: "Kevin",
    brideFull: "Tara Anindita Wibowo", groomFull: "Kevin Adrian Halim",
    brideParents: "Putri dari\nBapak Hendra Wibowo & Ibu Lydia Santoso", groomParents: "Putra dari\nBapak Robert Halim & Ibu Maria Gunawan",
    bridePhoto: "/themes/img/a127.webp", groomPhoto: "/themes/img/a126.webp",
    note: "Bata demi bata, lagu demi lagu: kami membangun rumah yang hangat untuk berdua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T15:00:00+07:00",
  place: "Loft Pabrik Tenun 1928",
  address: "Jl. Cicendo No. 14, Arjuna, Cicendo, Kota Bandung",
  stories: [
    { date: "2020", title: "Malam Open Mic", body: "Tara menyanyi di panggung kecil sebuah kafe loft di Braga. Kevin, pengiring gitar malam itu, lupa kunci lagu karena terlalu fokus mendengarkan." },
    { date: "2022", title: "Satu Studio", body: "Kami menyewa ruang kerja bersama di bekas gudang: dinding bata, jendela besi, dan terlalu banyak pot tanaman." },
    { date: "2026", title: "Lamaran", body: "Di bawah deretan bohlam yang Kevin pasang sendiri, ia memainkan lagu pertama kami lalu bertanya." },
    { date: "2027", title: "Hari Kami", body: "Kami merayakannya di loft tua yang kami cintai, bersama keluarga dan sahabat terdekat." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-09-25T15:00:00+07:00", time: "15.00 – 16.30 WIB", venue: "Loft Pabrik Tenun 1928", address: "Jl. Cicendo No. 14, Arjuna, Cicendo, Kota Bandung" },
    { name: "Resepsi", date: "2027-09-25T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Aula Bata, Loft Pabrik Tenun 1928", address: "Jl. Cicendo No. 14, Arjuna, Cicendo, Kota Bandung" },
  ],
  gallery: ["/themes/img/a139.webp", "/themes/img/a122.webp", "/themes/img/a127.webp", "/themes/img/a126.webp", "/themes/img/a140.webp", "/themes/img/a118.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0388 14", account_name: "Tara Anindita Wibowo" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2044 7781", account_name: "Kevin Adrian Halim" },
    { id: "demo-kado", type: "address", address: "Jl. Sukajadi No. 88, Unit 3B, Sukajadi, Kota Bandung 40162" },
  ],
  guestName: "Mas Bayu Pratama & Partner",
  guestTable: "Meja Jendela 4",
  extras: {
    rundown: { items: [
      { time: "18.30", title: "Welcome drink & akustik", note: "Trio jazz dari teman-teman Braga" },
      { time: "19.15", title: "Makan malam bersama" },
      { time: "20.00", title: "Dansa pertama & potong kue" },
      { time: "20.45", title: "Panggung terbuka untuk para sahabat" },
    ] },
    dressCode: { note: "Semi-formal bernuansa loft: hitam, abu beton, karamel, dan hijau daun.", colors: ["#1f1d1b", "#a7a39c", "#b5793e", "#467f3d"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Hendra Wibowo", "Kel. Robert Halim"] },
  },
});
