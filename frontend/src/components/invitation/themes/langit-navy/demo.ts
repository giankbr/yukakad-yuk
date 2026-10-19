import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gracia", groom: "Natanael",
    brideFull: "Gracia Anindya Putri, S.Ked.", groomFull: "Natanael Hendrawan, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak Yosef Hartanto & Ibu Maria Lusiana", groomParents: "Putra pertama dari\nBapak Daniel Hendrawan & Ibu Ruth Kristiani",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Di bawah langit yang sama, dua doa akhirnya bertemu dalam satu janji.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T15:00:00+07:00",
  place: "Rooftop Garden Langit Biru",
  address: "Jl. Mayjen Sungkono No. 89, Dukuh Pakis, Surabaya",
  stories: [
    { date: "Juli 2018", title: "Malam Observasi", body: "Bertemu di acara pengamatan gerhana bulan kampus. Teleskopnya cuma satu, antreannya panjang, obrolannya tak selesai sampai pagi." },
    { date: "2021", title: "Jarak & Rindu", body: "Gracia menempuh koas di Malang, Natanael bekerja di Surabaya. Setiap malam, bulan yang sama jadi pengingat." },
    { date: "Desember 2026", title: "Di Bawah Bintang", body: "Di sebuah bukit di Batu, Natanael berlutut dan bertanya. Bintang-bintang menjadi saksi jawaban Gracia." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-09-18T15:00:00+07:00", time: "15.00 – 16.30 WIB", venue: "GKI Bintang Timur", address: "Jl. Diponegoro No. 146, Darmo, Surabaya" },
    { name: "Resepsi Malam", date: "2027-09-18T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Rooftop Garden Langit Biru", address: "Jl. Mayjen Sungkono No. 89, Dukuh Pakis, Surabaya" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/a86.webp", "/themes/img/a87.webp", "/themes/img/a139.webp", "/themes/img/a38.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1420 0187 6543", account_name: "Natanael Hendrawan" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0813 3218 0918", account_name: "Gracia Anindya" },
  ],
  guestName: "Bapak Samuel Wijaya & Keluarga",
  guestTable: "7",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu.", source: "1 Korintus 13:4, 7" },
    rundown: { items: [
      { time: "15.00", title: "Pemberkatan nikah", note: "Keluarga & sahabat" },
      { time: "16.30", title: "Ramah tamah" },
      { time: "19.00", title: "Resepsi dibuka", note: "Welcome drink di rooftop" },
      { time: "20.30", title: "Dansa pertama & potong kue" },
    ] },
    dressCode: { note: "Nuansa malam: navy, hitam, atau keemasan.", colors: ["#13254a", "#0b1630", "#d6b46a", "#e9e4d6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Yosef Hartanto", "Kel. Besar Bpk. Daniel Hendrawan", "Persekutuan Pemuda GKI Bintang Timur"] },
    faq: { items: [
      { q: "Apakah resepsi di ruang terbuka?", a: "Ya, di rooftop dengan kanopi. Bila hujan, acara dipindah ke ballroom lantai yang sama." },
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir basement dan valet di lobi utama." },
    ] },
  },
});
