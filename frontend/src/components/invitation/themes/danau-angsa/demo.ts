import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Bima",
    brideFull: "Nadia Kirana Larasati", groomFull: "Bima Adiwangsa Prasetya",
    brideParents: "Putri kedua dari\nBapak Hendra Wijaya & Ibu Ratna Kusumadewi", groomParents: "Putra pertama dari\nBapak Agus Prasetya & Ibu Lina Marlina",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti sepasang angsa di danau yang tenang: setia, berdampingan, dan selalu kembali satu sama lain.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T15:00:00+07:00",
  place: "Lakeside Garden Patenggang",
  address: "Jl. Raya Ciwidey–Patenggang Km 39, Patengan, Rancabali, Kabupaten Bandung",
  stories: [
    { date: "2019", title: "Pagi Berkabut", body: "Kami bertemu dalam perjalanan fotografi ke Situ Patenggang. Kabut belum turun, kopi sudah dingin, obrolan tak selesai-selesai." },
    { date: "2023", title: "Musim yang Sama", body: "Jarak Bandung–Jakarta kami tempuh setiap akhir pekan, sampai rasanya kereta tahu nama kami." },
    { date: "2026", title: "Di Tepi Danau", body: "Di dermaga kayu tempat kami pertama bertemu, Bima bertanya, dan Kirana menjawab ya." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-06-12T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Dermaga Taman Danau", address: "Lakeside Garden Patenggang, Jl. Raya Ciwidey–Patenggang Km 39, Rancabali, Kabupaten Bandung" },
    { name: "Resepsi Senja", date: "2027-06-12T17:00:00+07:00", time: "17.00 – 20.00 WIB", venue: "Paviliun Willow", address: "Lakeside Garden Patenggang, Jl. Raya Ciwidey–Patenggang Km 39, Rancabali, Kabupaten Bandung" },
  ],
  gallery: ["/themes/img/r8.webp", "/themes/img/r1.webp", "/themes/img/r104.webp", "/themes/img/r15.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "3421 0098 77", account_name: "Nadia Kirana Larasati" },
    { id: "demo-kado", type: "address", address: "Jl. Dago Asri II No. 12, Dago, Coblong, Kota Bandung 40135" },
  ],
  guestName: "Ibu Maria Susanti & Keluarga",
  guestTable: "Meja Angsa 3",
  extras: {
    quote: { text: "Cinta itu sabar dan tenang seperti danau di pagi hari; ia tidak tergesa, namun selalu memantulkan langit yang sama.", source: "Kirana & Bima" },
    rundown: { items: [
      { time: "15.00", title: "Prosesi di dermaga", note: "Tamu dimohon hadir 30 menit sebelumnya" },
      { time: "16.00", title: "Teh sore di taman" },
      { time: "17.00", title: "Resepsi & makan malam", note: "Paviliun Willow" },
      { time: "19.00", title: "Lentera di tepi danau" },
    ] },
    dressCode: { note: "Semi formal bernuansa pastel: dusty blue, blush, sage, dan putih gading. Disarankan alas kaki datar, acara di atas rumput.", colors: ["#8ea8b6", "#f1cfc6", "#93ac8f", "#fbf5f1"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak Hendra Wijaya", "Kel. Besar Bapak Agus Prasetya"] },
    travel: { note: "Lokasi di dataran tinggi Ciwidey, udara sejuk menjelang sore. Bawa jaket tipis.", items: [
      { name: "Shuttle dari Kota Bandung", detail: "Berangkat 12.00 dari Jl. Dago, kembali 20.30" },
      { name: "Penginapan terdekat", detail: "Glamping & cottage di area Rancabali, ± 5 menit" },
    ] },
  },
});
