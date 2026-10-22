import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Natalia", groom: "Yosias",
    brideFull: "Natalia Mambrasar, S.Kep.", groomFull: "Yosias Dimara, S.Pi.",
    brideParents: "Putri ketiga dari\nBapak Korneles Mambrasar & Ibu Yuliana Wanma", groomParents: "Putra kedua dari\nBapak Hendrik Dimara & Ibu Ester Sauyai",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti pulau-pulau karang yang berdiri tenang di laut yang sama, kami dipertemukan Tuhan untuk saling menjaga.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T10:00:00+09:00",
  place: "Pantai WTC Waisai",
  address: "Jl. Pantai Waisai Torang Cinta, Waisai, Kabupaten Raja Ampat, Papua Barat Daya",
  stories: [
    { date: "2021", title: "Snorkeling di Arborek", body: "Natalia sedang praktik di puskesmas kampung, Yosias memandu tim survei terumbu karang. Satu perahu, satu sore yang tidak terlupakan." },
    { date: "2024", title: "Naik ke Piaynemo", body: "Di puncak tangga Piaynemo, di depan gugusan pulau karst yang berjajar, Yosias mengajak Natalia berjalan bersama ke depan." },
    { date: "2027", title: "Pulang ke Waisai", body: "Dengan restu kedua keluarga dan berkat Tuhan, kami siap menjadi satu rumah di tanah kelahiran kami." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-08-14T10:00:00+09:00", time: "10.00 – 11.30 WIT", venue: "Gereja GKI Imanuel Waisai", address: "Jl. Bahari, Waisai Kota, Kabupaten Raja Ampat, Papua Barat Daya" },
    { name: "Resepsi di Tepi Pantai", date: "2027-08-14T16:00:00+09:00", time: "16.00 – 20.00 WIT", venue: "Pantai WTC Waisai", address: "Jl. Pantai Waisai Torang Cinta, Waisai, Kabupaten Raja Ampat" },
  ],
  gallery: ["/themes/img/r110.webp", "/themes/img/r15.webp", "/themes/img/r105.webp", "/themes/img/r107.webp", "/themes/img/r106.webp", "/themes/img/r13.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Papua", account_number: "1502 0418 7731", account_name: "Natalia Mambrasar" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4281 0100 6623 507", account_name: "Yosias Dimara" },
    { id: "demo-kado", type: "address", address: "Jl. Kurkapa No. 21, Waisai Kota, Kabupaten Raja Ampat 98482" },
  ],
  guestName: "Bapak Obaja Rumbekwan & Keluarga",
  guestTable: "Meja Arborek",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati. Kasih tidak berkesudahan.", source: "1 Korintus 13:4, 8" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu", note: "Tarian Wor & tifa" },
      { time: "17.00", title: "Ibadah syukur" },
      { time: "18.00", title: "Makan bersama saat matahari terbenam", note: "Ikan bakar, papeda & sagu lempeng" },
      { time: "19.00", title: "Yospan bersama di pasir" },
    ] },
    dressCode: { note: "Busana pantai yang rapi: putih, pasir, dan biru laut. Alas kaki nyaman untuk pasir.", colors: ["#f6f0df", "#2fb3b6", "#1f6f8a", "#e07b4f"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Mambrasar – Wanma", "Kel. Besar Dimara – Sauyai", "Jemaat GKI Imanuel Waisai"] },
  },
});
