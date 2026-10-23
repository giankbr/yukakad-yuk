import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinanti", groom: "Elang",
    brideFull: "Kinanti Maharani Soetomo, S.Sn.", groomFull: "Elang Pradipta Nugroho, S.Kom.",
    brideParents: "Putri kedua dari\nBapak Bambang Soetomo & Ibu Yuliana Kartika", groomParents: "Putra tunggal dari\nBapak Teguh Nugroho & Ibu Diah Permatasari",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Sisi A adalah dua orang asing di toko piringan hitam. Sisi B kami tulis bersama, mulai hari ini.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T17:00:00+07:00",
  place: "Ruang Swing, Kemang",
  address: "Jl. Kemang Raya No. 88, Bangka, Mampang Prapatan, Jakarta Selatan",
  stories: [
    { date: "Maret 2020", title: "Satu Piringan, Dua Tangan", body: "Kami meraih piringan hitam bekas yang sama di sebuah toko kecil di Blok M. Elang mengalah, Kinanti meminjamkannya seminggu kemudian." },
    { date: "2022", title: "Malam Jazz Kamis", body: "Setiap Kamis kami duduk di meja yang sama dekat panggung. Pemain bas sampai hafal pesanan kami: teh jahe dan kentang goreng." },
    { date: "Juni 2027", title: "Lagu yang Diputar Pelan", body: "Elang meminta band memainkan lagu pertama yang kami dengar bersama, lalu berlutut sebelum lagunya selesai." },
  ],
  events: [
    { name: "Upacara Janji Nikah", date: "2027-09-18T17:00:00+07:00", time: "17.00 – 18.00 WIB", venue: "Galeri Atas, Ruang Swing", address: "Jl. Kemang Raya No. 88, Bangka, Mampang Prapatan, Jakarta Selatan" },
    { name: "Resepsi Malam Jazz", date: "2027-09-18T19:00:00+07:00", time: "19.00 – 22.30 WIB", venue: "Panggung Utama, Ruang Swing", address: "Jl. Kemang Raya No. 88, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/a132.webp", "/themes/img/a133.webp", "/themes/img/a140.webp", "/themes/img/r93.webp", "/themes/img/a122.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0938 46", account_name: "Kinanti Maharani Soetomo" },
    { id: "demo-cimb", type: "bank", bank_name: "CIMB Niaga", account_number: "7060 1122 9835", account_name: "Elang Pradipta Nugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka Raya No. 21, Pela Mampang, Mampang Prapatan, Jakarta Selatan 12720" },
  ],
  guestName: "Bapak Antonius Wibisono & Keluarga",
  guestTable: "Meja Saksofon 5",
  extras: {
    quote: { text: "Cinta yang baik seperti lagu jazz yang baik: tidak selalu sesuai partitur, tetapi selalu kembali ke nada dasarnya.", source: "Catatan sampul Kinanti & Elang" },
    rundown: { items: [
      { time: "19.00", title: "Pembukaan oleh trio jazz", note: "Panggung Utama" },
      { time: "19.30", title: "Kedua mempelai memasuki ruangan" },
      { time: "20.00", title: "Makan malam & sesi lagu permintaan" },
      { time: "21.15", title: "Dansa pertama, lalu lantai dansa dibuka" },
    ] },
    dressCode: { note: "Malam klub jazz: navy, hitam, mustard, krem. Jas atau gaun selutut, sepatu yang siap berdansa swing.", colors: ["#16233d", "#d9a532", "#f3e6c8", "#b5532f", "#0c1426"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Bambang Soetomo", "Kel. Besar Bpk. Teguh Nugroho"] },
    travel: { note: "Kawasan Kemang padat di malam Sabtu. Gunakan transportasi daring bila memungkinkan.", items: [
      { name: "Parkir", detail: "Gedung parkir di sebelah Ruang Swing, tersedia valet" },
      { name: "Menginap", detail: "Beberapa hotel di Jl. Kemang Raya, ± 5 menit berjalan kaki" },
    ] },
  },
});
