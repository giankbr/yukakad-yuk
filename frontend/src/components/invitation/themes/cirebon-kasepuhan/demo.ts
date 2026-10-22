import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Larasati", groom: "Raka",
    brideFull: "Larasati Ayu Wulandari, S.Ds.", groomFull: "Elang Raka Aditya Pratama, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Sudarsono & Ibu Hj. Ratnaningsih",
    groomParents: "Putra pertama dari\nBapak Elang Mukhtar Hidayat & Ibu Hj. Yuyun Sumarni",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti piring-piring porselen yang dirangkai di dinding bata keraton, dua keluarga kami kini menyatu dalam satu gerbang.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-19T11:00:00+07:00",
  place: "Pendopo Taman Sari Grage",
  address: "Jl. Kesambi Raya No. 21, Kesambi, Kota Cirebon",
  stories: [
    { date: "2019", title: "Pameran Batik Trusmi", body: "Laras menjaga stan batik keluarganya, Raka datang mencari kain untuk ibunya. Ia pulang membawa dua lembar kain dan satu nomor telepon." },
    { date: "2024", title: "Ta'aruf", body: "Setelah lama berteman, kami saling mengenal dengan niat baik, didampingi keluarga dan guru ngaji Laras." },
    { date: "Februari 2027", title: "Lamaran", body: "Keluarga Raka datang membawa seserahan, sirih pinang, dan empal gentong kesukaan Bapak. Lamaran diterima dengan penuh syukur." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sang Cipta Rasa", address: "Jl. Kasepuhan No. 43, Lemahwungkuk, Kota Cirebon" },
    { name: "Resepsi", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Taman Sari Grage", address: "Jl. Kesambi Raya No. 21, Kesambi, Kota Cirebon" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a31.webp", "/themes/img/a64.webp", "/themes/img/a22.webp", "/themes/img/r16.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 4483 19", account_name: "Larasati Ayu Wulandari" },
    { id: "demo-bjb", type: "bank", bank_name: "BJB Syariah", account_number: "0051 2290 7731", account_name: "Elang Raka Aditya Pratama" },
    { id: "demo-kado", type: "address", address: "Jl. Pulasaren Gg. Kenari No. 7, Pekalipan, Kota Cirebon 45116", account_name: "Keluarga H. Sudarsono" },
  ],
  guestName: "Bapak H. Abdul Somad & Keluarga",
  guestTable: "Meja Sunyaragi 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin", note: "Diiringi gamelan Cirebonan" },
      { time: "11.30", title: "Doa & sambutan keluarga" },
      { time: "12.00", title: "Santap siang", note: "Nasi jamblang & empal gentong" },
      { time: "13.00", title: "Foto bersama", note: "Per rombongan" },
    ] },
    dressCode: { note: "Batik Cirebonan atau busana muslim bernuansa bata merah, biru porselen, dan putih kapur.", colors: ["#b4482e", "#2c4f9a", "#f4ede1", "#c9bda7"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Sudarsono", "Kel. Besar Elang Mukhtar Hidayat"] },
  },
});
