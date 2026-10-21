import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Raka",
    brideFull: "Nadia Putri Rahmawati, S.Ds.", groomFull: "Raka Aditya Nugraha, S.T.",
    brideParents: "Putri dari Bapak Agus Rahmat & Ibu Dewi Kartika", groomParents: "Putra dari Bapak Hendra Nugraha & Ibu Sri Wulandari",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Dua garis yang berbeda, satu bidang yang sama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-11T08:00:00+07:00",
  place: "Selasar Sunaryo Art Space",
  address: "Jl. Bukit Pakar Timur No. 100, Ciburial, Cimenyan, Kabupaten Bandung",
  stories: [
    { date: "2019", title: "Satu meja di studio", body: "Nadia mendesain interior, Raka menghitung strukturnya. Proyek pertama kami: sebuah kafe kecil di Dago." },
    { date: "2024", title: "Rumah kecil, rencana besar", body: "Kami mulai menggambar denah rumah impian di balik kertas kalkir sisa kantor." },
    { date: "2027", title: "Babak baru", body: "Dengan restu kedua keluarga, kami memutuskan membangun semuanya bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung" },
    { name: "Resepsi", date: "2027-09-11T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Selasar Sunaryo Art Space", address: "Jl. Bukit Pakar Timur No. 100, Ciburial, Cimenyan, Kabupaten Bandung" },
  ],
  gallery: ["/themes/img/a78.webp", "/themes/img/r91.webp", "/themes/img/r90.webp", "/themes/img/r72.webp", "/themes/img/r79.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "7810 2245 63", account_name: "Nadia Putri Rahmawati" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2045 7788", account_name: "Raka Aditya Nugraha" },
  ],
  guestName: "Saudari Anindya Prameswari",
  guestTable: "B4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penerimaan tamu", note: "Amfiteater" },
      { time: "11.30", title: "Kirab pengantin" },
      { time: "12.00", title: "Makan siang & akustik" },
      { time: "13.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Smart casual dalam nuansa sage, terakota, dan krem.", colors: ["#9fb19a", "#c77653", "#e0bf98", "#efe8dc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Agus Rahmat", "Kel. Besar Bpk. Hendra Nugraha"] },
  },
});
