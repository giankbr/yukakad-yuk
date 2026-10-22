import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sri", groom: "Harjono",
    brideFull: "Hj. Sri Rahayu Ningsih", groomFull: "H. Raden Harjono Wiryosuparto",
    brideParents: "Pensiunan guru SD Negeri 2 Klaten,\npembuat jenang paling enak se-kampung", groomParents: "Pensiunan mantri kesehatan,\npenjaga kebun mangga di belakang rumah",
    bridePhoto: "/themes/img/r53.webp", groomPhoto: "/themes/img/r52.webp",
    note: "Lima puluh tahun lalu Eyang Kakung dan Eyang Putri berjanji di Klaten dengan sederhana. Hari ini anak, cucu, dan cicit ingin mensyukurinya bersama Bapak/Ibu/Saudara/i yang menemani perjalanan itu.",
  },
  eventLabel: "Syukuran 50 Tahun Pernikahan",
  date: "2027-07-16T16:00:00+07:00",
  place: "Kediaman Keluarga Harjono",
  address: "Jl. Pemuda Selatan No. 21, Klaten Tengah, Kabupaten Klaten, Jawa Tengah",
  stories: [
    { date: "1977", title: "Ijab di Rumah Simbah", body: "Eyang Kakung, mantri muda di puskesmas, menikahi Eyang Putri, guru SD yang baru diangkat. Tenda bambu, gamelan tetangga, dan nasi tumpeng." },
    { date: "1979 – 1988", title: "Lima Anak, Satu Sepeda", body: "Bambang, Ratih, Dwi, Wulan, dan Agus lahir berurutan. Sepeda onthel Eyang Kakung jadi kendaraan untuk mengantar semuanya sekolah." },
    { date: "2002", title: "Cucu Pertama", body: "Rumah kembali ramai tangis bayi. Sejak itu, setiap Lebaran meja makan harus disambung dua." },
    { date: "2027", title: "Lima Puluh Tahun", body: "Rambut sudah putih semua, tetapi Eyang masih minum teh berdua setiap sore di teras, seperti dulu." },
  ],
  events: [
    { name: "Pengajian & Doa Syukur", date: "2027-07-16T16:00:00+07:00", time: "16.00 – 17.30 WIB", venue: "Kediaman Keluarga Harjono", address: "Jl. Pemuda Selatan No. 21, Klaten Tengah, Kabupaten Klaten, Jawa Tengah" },
    { name: "Ramah Tamah & Makan Malam", date: "2027-07-16T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Kediaman Keluarga Harjono", address: "Jl. Pemuda Selatan No. 21, Klaten Tengah, Kabupaten Klaten, Jawa Tengah" },
  ],
  gallery: ["/themes/img/r54.webp", "/themes/img/r55.webp", "/themes/img/r53.webp", "/themes/img/r52.webp", "/themes/img/r56.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0217 0100 4471 509", account_name: "Bambang Harjono (untuk Panti Wreda)" },
  ],
  guestName: "Bapak Soetrisno & Keluarga",
  guestTable: "Meja Melati 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "16.00", title: "Pengajian dan doa syukur", note: "Dipimpin Ustaz Muh. Zaini" },
      { time: "18.30", title: "Sungkeman anak, cucu, dan cicit" },
      { time: "19.00", title: "Pemotongan tumpeng emas", note: "Diserahkan kepada cucu pertama" },
      { time: "19.30", title: "Makan malam & putar album kenangan" },
    ] },
    dressCode: { note: "Batik atau busana rapi bernuansa emas, krem, dan cokelat.", colors: ["#c9a04a", "#f5ecd8", "#4b2a19", "#d87a34"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Ir. Bambang Harjono", "Kel. dr. Ratih Harjono", "Kel. Dwi Harjono", "Kel. Wulan Harjono", "Kel. Agus Harjono", "Para cucu & cicit"] },
  },
});
