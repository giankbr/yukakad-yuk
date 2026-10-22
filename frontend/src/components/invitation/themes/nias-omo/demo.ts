import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kristin", groom: "Daniel",
    brideFull: "Kristin Yuliana Laia, S.Pd.", groomFull: "Daniel Arozatulo Zebua, S.Kom.",
    brideParents: "Putri sulung dari\nBapak Yustinus Laia & Ibu Martha Ndruru", groomParents: "Putra ketiga dari\nBapak Elisa Zebua & Ibu Rosmaini Harefa",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti tiang-tiang Omo Sebua yang saling menopang, kami ingin membangun rumah yang kokoh di atas kasih dan iman.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T10:00:00+07:00",
  place: "BNKP Jemaat Gunungsitoli Kota",
  address: "Jl. Sirao No. 2, Pasar Gunungsitoli, Kota Gunungsitoli, Sumatera Utara",
  stories: [
    { date: "2017", title: "Ombak Sorake", body: "Daniel sedang belajar berselancar di Pantai Sorake; Kristin datang bersama rombongan guru untuk pelatihan di Teluk Dalam." },
    { date: "2021", title: "Hombo Batu", body: "Kami menonton lompat batu di Bawömataluo. Di antara sorak warga desa, Daniel memberanikan diri menyatakan perasaannya." },
    { date: "2026", title: "Fame'e Li", body: "Keluarga Zebua datang membawa sirih dan menyampaikan pinangan. Kedua keluarga bersepakat dalam sukacita." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-10T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "BNKP Jemaat Gunungsitoli Kota", address: "Jl. Sirao No. 2, Pasar Gunungsitoli, Kota Gunungsitoli" },
    { name: "Resepsi", date: "2027-07-10T13:00:00+07:00", time: "13.00 – 16.00 WIB", venue: "Gedung Serbaguna Ya'ahowu", address: "Jl. Diponegoro No. 118, Ilir, Kota Gunungsitoli" },
    { name: "Pesta Adat Falöwa", date: "2027-07-17T10:00:00+07:00", time: "10.00 WIB – selesai", venue: "Omo Keluarga Zebua", address: "Jl. Pelabuhan No. 7, Pasar Teluk Dalam, Nias Selatan" },
  ],
  gallery: ["/themes/img/r10.webp", "/themes/img/r15.webp", "/themes/img/r107.webp", "/themes/img/r106.webp", "/themes/img/r109.webp", "/themes/img/r105.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0210 0100 5566 504", account_name: "Kristin Yuliana Laia" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "107 00 1122334 5", account_name: "Daniel Arozatulo Zebua" },
    { id: "demo-kado", type: "address", address: "Jl. Karet No. 9, Ilir, Kota Gunungsitoli 22815" },
  ],
  guestName: "Bapak Faozanolo Gulö & Keluarga",
  guestTable: "Meja Bawömataluo 5",
  extras: {
    rundown: { items: [
      { time: "13.00", title: "Penyambutan pengantin", note: "Diiringi tari Maena bersama" },
      { time: "13.30", title: "Kata sambutan & doa" },
      { time: "14.00", title: "Makan bersama", note: "Gowi nifufu dan ikan bakar" },
      { time: "15.00", title: "Maena & foto keluarga" },
    ] },
    dressCode: { note: "Busana resmi atau bernuansa adat Nias. Hitam, merah, dan kuning keemasan dipersilakan.", colors: ["#151010", "#a3241c", "#e2b02a", "#c99a3c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-10T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Laia – Ndruru (Gunungsitoli)", "Kel. Besar Zebua – Harefa (Teluk Dalam)"] },
  },
});
