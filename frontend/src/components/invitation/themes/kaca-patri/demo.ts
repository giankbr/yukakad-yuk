import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Clarissa", groom: "Gabriel",
    brideFull: "Maria Clarissa Wulandari, S.Ars.", groomFull: "Yohanes Gabriel Pratama, S.T., M.T.",
    brideParents: "Putri pertama dari\nBapak Antonius Hadi Susilo & Ibu Theresia Wulan Sari", groomParents: "Putra ketiga dari\nBapak Fransiskus Bambang Pratama & Ibu Agnes Sri Lestari",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Seperti cahaya yang menembus kaca warna-warni, kasih membuat hal-hal biasa menjadi bercahaya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-20T10:00:00+07:00",
  place: "Hotel Savoy Homann",
  address: "Jl. Asia Afrika No. 112, Cikawao, Lengkong, Bandung",
  stories: [
    { date: "2017", title: "Kelas Restorasi Bangunan", body: "Clarissa memotret jendela kaca patri gereja tua di Braga, Gabriel mengukur kusen kayunya." },
    { date: "2021", title: "Proyek Bersama", body: "Kami merestorasi sebuah kapel kecil di Lembang, panel demi panel, selama sembilan bulan." },
    { date: "2026", title: "Lamaran", body: "Di bawah jendela kapel yang kami pulihkan, Gabriel bertanya dan cahaya sore menjawab lebih dulu." },
  ],
  events: [
    { name: "Sakramen Perkawinan", date: "2027-11-20T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "Gereja Katedral Santo Petrus", address: "Jl. Merdeka No. 14, Babakan Ciamis, Sumur Bandung, Bandung" },
    { name: "Resepsi", date: "2027-11-20T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Hotel Savoy Homann", address: "Jl. Asia Afrika No. 112, Cikawao, Lengkong, Bandung" },
  ],
  gallery: ["/themes/img/a86.webp", "/themes/img/a43.webp", "/themes/img/a87.webp", "/themes/img/a139.webp", "/themes/img/a140.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 2291 88", account_name: "Maria Clarissa Wulandari" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0912 3345 67", account_name: "Yohanes Gabriel Pratama" },
    { id: "demo-kado", type: "address", address: "Jl. Braga No. 37, Sumur Bandung, Bandung 40111" },
  ],
  guestName: "Bapak Robertus Santoso & Keluarga",
  guestTable: "Meja Lili 6",
  extras: {
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Lobi art deco" },
      { time: "19.00", title: "Prosesi masuk & doa makan" },
      { time: "19.30", title: "Santap malam & kuartet gesek" },
      { time: "20.45", title: "Potong kue & foto bersama" },
    ] },
    dressCode: { note: "Formal dengan nuansa permata: rubi, safir, zamrud, atau amber.", colors: ["#a81f38", "#1d4a9e", "#2a7d55", "#e3a93e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-11-20T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Antonius Hadi Susilo", "Kel. Besar Bpk. Fransiskus Bambang Pratama"] },
  },
});
