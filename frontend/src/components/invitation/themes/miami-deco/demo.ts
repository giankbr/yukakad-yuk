import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Amanda", groom: "Kevin",
    brideFull: "Amanda Kirana Putri", groomFull: "Kevin Hartanto Wijaya",
    brideParents: "Putri bungsu dari\nBapak Stefanus Halim & Ibu Lenny Susanti", groomParents: "Putra kedua dari\nBapak Robert Wijaya & Ibu Grace Natalia",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Matahari, pasir, dan kamu. Ayo rayakan babak baru kami di tepi pantai!",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T16:00:00+08:00",
  place: "Paviliun Laguna Sanur",
  address: "Jl. Danau Tamblingan No. 88, Sanur Kauh, Denpasar Selatan, Bali",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Antre Es Krim", body: "Kami bertemu di antrean kedai es krim saat liburan kantor di Sanur. Amanda memilih rasa stroberi, Kevin memilih mint. Sejak itu kami suka berbagi dua rasa." },
    { date: "2025", title: "Layang-Layang di Pantai", body: "Setiap akhir pekan kami bermain layang-layang di pantai. Suatu sore, di ekor layang-layang Kevin tergantung sebuah cincin." },
    { date: "2027", title: "Pesta di Tepi Pantai", body: "Kini kami mengundang keluarga dan sahabat untuk berpesta bersama di bawah langit biru Sanur." },
  ],
  events: [
    { name: "Pemberkatan Pernikahan", date: "2027-05-22T16:00:00+08:00", time: "16.00 – 17.00 WITA", venue: "Taman Pantai Paviliun Laguna", address: "Jl. Danau Tamblingan No. 88, Sanur Kauh, Denpasar Selatan, Bali" },
    { name: "Pesta Pantai", date: "2027-05-22T18:00:00+08:00", time: "18.00 – 22.00 WITA", venue: "Teras Laguna, Paviliun Laguna Sanur", address: "Jl. Danau Tamblingan No. 88, Sanur Kauh, Denpasar Selatan, Bali" },
  ],
  gallery: ["/themes/img/r103.webp", "/themes/img/r85.webp", "/themes/img/r110.webp", "/themes/img/r100.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0881 2457 90", account_name: "Amanda Kirana Putri" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 3301 7720", account_name: "Kevin Hartanto Wijaya" },
  ],
  guestName: "Mbak Tasya & Partner",
  guestTable: "Kamar 204",
  extras: {
    quote: { text: "Rumah bukanlah sebuah tempat, melainkan seseorang yang membuatmu ingin pulang.", source: "Amanda & Kevin" },
    rundown: { items: [
      { time: "16.00", title: "Pemberkatan di taman pantai" },
      { time: "17.00", title: "Mocktail senja & foto bersama", note: "Booth foto bertema retro" },
      { time: "18.00", title: "Makan malam & pesta dansa" },
      { time: "21.30", title: "Kembang api kecil di pantai" },
    ] },
    dressCode: { note: "Pastel ceria: merah muda, mint, kuning lemon, dan lavender. Kemeja motif tropis dipersilakan.", colors: ["#f4a9bb", "#a6e3cf", "#f8e189", "#c9b6ea"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-22T16:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Stefanus Halim", "Kel. Besar Bpk. Robert Wijaya"] },
    faq: { items: [
      { q: "Apakah acara di luar ruangan?", a: "Ya, di taman dan teras tepi pantai. Bawa kacamata hitam dan alas kaki yang nyaman." },
      { q: "Apakah ada parkir?", a: "Parkir tersedia di area Paviliun Laguna, dengan petugas valet di lobi." },
    ] },
  },
});
