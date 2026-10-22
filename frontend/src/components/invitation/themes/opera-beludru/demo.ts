import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Amara", groom: "Kenzo",
    brideFull: "Amara Valencia Hartono, B.Mus.",
    groomFull: "Kenzo Mahardika Lim",
    brideParents: "Putri dari\nBapak Robert Hartono & Ibu Melinda Sasmita",
    groomParents: "Putra dari\nBapak Hendrik Lim & Ibu Yuliana Kartika",
    bridePhoto: "/themes/img/a83.webp",
    groomPhoto: "/themes/img/a84.webp",
    note: "Seorang penyanyi sopran dan pemain cello yang bertemu di balik panggung, kini memainkan satu partitur bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-20T16:00:00+07:00",
  place: "Gedung Kesenian Jakarta",
  address: "Jl. Gedung Kesenian No. 1, Pasar Baru, Sawah Besar, Jakarta Pusat",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Babak I · 2018", title: "Di balik panggung", body: "Malam pementasan opera kampus, Amara lupa naskah aria dan Kenzo meminjamkan partitur cadangannya dari bangku orkestra." },
    { date: "Babak II · 2022", title: "Duet pertama", body: "Konser amal di Bandung: satu lagu, satu sopran, satu cello. Penonton mengira kami sudah lama berpasangan." },
    { date: "Babak III · 2027", title: "Lamaran saat tirai turun", body: "Usai resital tunggal Amara, Kenzo naik ke panggung membawa buket mawar merah dan sebuah cincin." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-11-20T16:00:00+07:00", time: "16.00 – 17.30 WIB", venue: "Foyer Gedung Kesenian Jakarta", address: "Jl. Gedung Kesenian No. 1, Pasar Baru, Sawah Besar, Jakarta Pusat" },
    { name: "Resepsi Gala", date: "2027-11-20T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Auditorium Gedung Kesenian Jakarta", address: "Jl. Gedung Kesenian No. 1, Pasar Baru, Sawah Besar, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/a86.webp", "/themes/img/a122.webp", "/themes/img/a87.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "0613 2277 90", account_name: "Amara Valencia Hartono" },
    { id: "demo-kado", type: "address", address: "Jl. Kertanegara No. 18, Selong, Kebayoran Baru, Jakarta Selatan 12110" },
  ],
  guestName: "Bapak Antonius Gunawan & Partner",
  guestTable: "Loge 3",
  extras: {
    quote: { text: "Musik dimulai ketika kata-kata tak lagi sanggup. Begitu pula cinta.", source: "Catatan di partitur kami" },
    rundown: { items: [
      { time: "16.00", title: "Ouverture: upacara pernikahan", note: "Diiringi kuartet gesek" },
      { time: "18.30", title: "Foyer dibuka, minuman sambutan" },
      { time: "19.00", title: "Resepsi gala & makan malam" },
      { time: "20.30", title: "Aria persembahan", note: "Duet sopran & cello oleh kedua mempelai" },
    ] },
    dressCode: { note: "Black tie: gaun malam dan jas gelap. Aksen merah beludru atau emas dipersilakan.", colors: ["#7a0f1c", "#1a0a0c", "#c9a04e", "#f4ead6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Keluarga Besar Hartono", "Keluarga Besar Lim", "Orkes Kamar Sasmita"] },
    faq: { items: [
      { q: "Apakah ada tempat parkir?", a: "Parkir valet tersedia di depan gedung; parkir umum di area Pasar Baru." },
      { q: "Kapan sebaiknya tiba?", a: "Pintu foyer dibuka 30 menit sebelum acara. Mohon tiba tepat waktu agar tirai dapat dibuka bersama." },
    ] },
  },
});
