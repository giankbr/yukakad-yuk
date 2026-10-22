import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Bayu",
    brideFull: "Ni Komang Sekar Wulandari, S.Sn.", groomFull: "I Gede Bayu Adnyana, S.T.",
    brideParents: "Putri kedua dari\nBapak I Nyoman Suarsa & Ibu Ni Wayan Rasmini", groomParents: "Putra pertama dari\nBapak I Ketut Darma Yasa & Ibu Ni Made Sriani",
    bridePhoto: "/themes/img/a62.webp", groomPhoto: "/themes/img/a60.webp",
    note: "Seperti benang gringsing yang diikat dan dicelup berkali-kali, semoga ikatan kami kuat, sabar, dan terjaga dari segala sakit.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-07-17T09:00:00+08:00",
  place: "Desa Adat Tenganan Pegringsingan",
  address: "Desa Tenganan, Kec. Manggis, Kabupaten Karangasem, Bali",
  stories: [
    { date: "2019", title: "Benang Pertama", body: "Sekar belajar menenun di bale keluarganya. Bayu datang memotret, lalu lebih sering datang daripada memotret." },
    { date: "2024", title: "Ngidih", body: "Keluarga Bayu datang memohon dengan tata krama adat. Kedua keluarga sepakat, para tetua memilih dewasa ayu." },
    { date: "2027", title: "Pawiwahan", body: "Di hadapan keluarga, desa adat, dan Ida Sang Hyang Widhi Wasa, kami mengikat janji sehidup semati." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-07-17T09:00:00+08:00", time: "09.00 – 12.00 WITA", venue: "Kediaman Mempelai Pria", address: "Jl. Desa Tenganan No. 8, Tenganan, Kec. Manggis, Karangasem, Bali" },
    { name: "Resepsi", date: "2027-07-17T18:00:00+08:00", time: "18.00 – 21.00 WITA", venue: "Wantilan Desa Tenganan", address: "Desa Tenganan Pegringsingan, Kec. Manggis, Karangasem, Bali" },
  ],
  gallery: ["/themes/img/a61.webp", "/themes/img/r108.webp", "/themes/img/a62.webp", "/themes/img/a60.webp", "/themes/img/r109.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "018 02 11 22334 4", account_name: "Ni Komang Sekar Wulandari" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0921 4455 66", account_name: "I Gede Bayu Adnyana" },
  ],
  guestName: "Bapak I Made Sudarsana & Keluarga",
  guestTable: "Bale 3",
  extras: {
    quote: { text: "Wahai pasangan suami-istri, semoga kalian tetap bersatu dan tidak pernah terpisahkan. Semoga kalian mencapai hidup yang penuh kebahagiaan, tinggal di rumah yang penuh kegembiraan bersama seluruh keturunanmu.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "09.00", title: "Mekala-kalaan", note: "Upacara penyucian kedua mempelai" },
      { time: "10.30", title: "Mejaya-jaya & natab banten" },
      { time: "11.30", title: "Ramah tamah keluarga", note: "Megibung bersama" },
    ] },
    dressCode: { note: "Busana adat madya Bali. Merah, hitam, dan krem dipersilakan.", colors: ["#7a2619", "#24130f", "#e9d8b4", "#a8432a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-17T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar I Nyoman Suarsa", "Kel. Besar I Ketut Darma Yasa", "Krama Desa Adat Tenganan"] },
  },
});
