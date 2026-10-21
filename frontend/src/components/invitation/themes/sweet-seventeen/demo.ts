import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aurel", groom: "",
    brideFull: "Aurelia Putri Maheswari",
    brideParents: "Putri sulung dari Bapak Reza Maheswara & Ibu Clarissa Wijaya",
    bridePhoto: "/themes/img/a127.webp",
    note: "Satu malam berkilau untuk merayakan tujuh belas tahun, bersama orang-orang yang paling berarti.",
  },
  eventLabel: "Sweet Seventeen",
  date: "2027-11-06T19:00:00+07:00",
  place: "Ballroom Kaca, Hotel Arunika",
  address: "Jl. Raya Darmo No. 88, Wonokromo, Surabaya",
  story: { title: "Tujuh Belas Tahun", body: "" },
  stories: [
    { date: "2010", title: "Hadiah terindah", body: "Lahir di bulan November yang hujan, membawa terang bagi Papa dan Mama." },
    { date: "2016", title: "Sepatu balet pertama", body: "Tutu merah muda, pita satin, dan penampilan pertama yang membuat semua bertepuk tangan." },
    { date: "2023", title: "Panggung paduan suara", body: "Menyanyi solo di lomba paduan suara pelajar se-Jawa Timur, gugup tapi bangga." },
    { date: "2027", title: "Tujuh belas", body: "Siap melangkah ke babak baru, dengan mimpi kuliah desain dan hati yang penuh syukur." },
  ],
  events: [
    { name: "Sweet Seventeen Dinner Party", date: "2027-11-06T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Ballroom Kaca, Hotel Arunika", address: "Jl. Raya Darmo No. 88, Wonokromo, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "8830 2711 06", account_name: "Clarissa Wijaya" },
  ],
  guestName: "Kak Nadine & Partner",
  guestTable: "Meja Mutiara 3",
  extras: {
    child: { name: "Aurelia Putri Maheswari", nickname: "Aurel", birthDate: "2010-11-06T08:20:00+07:00", photo: "/themes/img/a127.webp", parents: "Putri sulung dari Bapak Reza Maheswara & Ibu Clarissa Wijaya" },
    rundown: { items: [
      { time: "19.00", title: "Karpet merah muda & photo booth", note: "Ambil kartu meja di meja tamu" },
      { time: "19.45", title: "Pembukaan & dansa pertama bersama Papa" },
      { time: "20.15", title: "Upacara 17 lilin", note: "Untuk 17 orang istimewa" },
      { time: "20.45", title: "Makan malam & tiup lilin" },
    ] },
    dressCode: { note: "Glam semi-formal bernuansa merah muda, putih, atau mutiara.", colors: ["#f2a9c4", "#fbe9ef", "#e9e0da", "#2a1236"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Dengan hangat mengundang", names: ["Papa Reza & Mama Clarissa", "Opa & Oma Wijaya", "Adik Kenzo"] },
    faq: { items: [
      { q: "Boleh datang bersama pasangan?", a: "Boleh, mohon isi jumlah tamu di form kehadiran ya." },
      { q: "Apakah ada parkir?", a: "Tersedia valet dan parkir basement Hotel Arunika." },
    ] },
  },
});
