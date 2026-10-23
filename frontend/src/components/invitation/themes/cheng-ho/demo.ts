import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Yusuf",
    brideFull: "Siti Aisyah Liem, S.E.", groomFull: "Muhammad Yusuf Ong, S.Kom.",
    brideParents: "Putri pertama dari\nBapak H. Abdul Karim Liem & Ibu Hj. Maryam Tan", groomParents: "Putra kedua dari\nBapak H. Ibrahim Ong & Ibu Hj. Fatimah Lie",
    note: "Dua keluarga, dua tradisi, satu niat: membangun rumah tangga yang sakinah dalam naungan ridha Allah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T09:00:00+07:00",
  place: "Hotel Majapahit Surabaya",
  address: "Jl. Tunjungan No. 65, Genteng, Kota Surabaya",
  stories: [
    { date: "2018", title: "Kajian Remaja Masjid", body: "Kami bertemu di kajian Ahad pagi untuk muslim Tionghoa muda di Surabaya. Aisyah mencatat, Yusuf menyiapkan teh." },
    { date: "2022", title: "Ramadan Bersama", body: "Bertahun-tahun menjadi panitia buka puasa bersama di masjid, dari menata takjil sampai mencuci gelas." },
    { date: "2026", title: "Lamaran", body: "Kedua keluarga bertemu di meja bundar, lengkap dengan teh melati dan kue lapis legit buatan Oma." },
    { date: "2027", title: "Akad", body: "Dengan restu orang tua, kami mengikat janji di masjid tempat kami pertama bertemu." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Muhammad Cheng Hoo", address: "Jl. Gading No. 2, Ketabang, Genteng, Kota Surabaya" },
    { name: "Resepsi", date: "2027-10-16T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Hotel Majapahit Surabaya", address: "Jl. Tunjungan No. 65, Genteng, Kota Surabaya" },
  ],
  gallery: ["/themes/img/a123.webp", "/themes/img/r57.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0881 2345 67", account_name: "Siti Aisyah Liem" },
    { id: "demo-kado", type: "address", address: "Jl. Kembang Jepun No. 41, Bongkaran, Pabean Cantian, Surabaya 60161" },
  ],
  guestName: "Keluarga Bapak H. Hasan Tjoa",
  guestTable: "Meja Bundar 8",
  extras: {
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Iringan gambang kromong instrumental" },
      { time: "19.00", title: "Tilawah & doa" },
      { time: "19.20", title: "Jamuan halal", note: "Bakmi panjang umur, lontong cap go meh, dan es kacang merah" },
      { time: "20.15", title: "Foto bersama keluarga besar" },
    ] },
    dressCode: { note: "Busana muslim formal atau cheongsam muslimah. Merah, hijau giok, dan emas dipersilakan.", colors: ["#b8322a", "#2f6d57", "#d6a64a", "#f5ecd9"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Karim Liem", "Kel. Besar H. Ibrahim Ong"] },
  },
});
