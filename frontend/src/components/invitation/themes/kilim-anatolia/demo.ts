import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Fikri",
    brideFull: "Zahra Aulia Nasution, S.Hum.", groomFull: "Muhammad Fikri Ramadhan, M.A.",
    brideParents: "Putri kedua dari\nBapak H. Irwan Nasution & Ibu Hj. Ratna Siregar", groomParents: "Putra pertama dari\nBapak Drs. H. Agus Salim & Ibu Hj. Nurlaila",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti benang lungsin dan pakan, kami dipertemukan Allah untuk saling menguatkan menjadi satu tenunan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Hotel Savoy Homann",
  address: "Jl. Asia Afrika No. 112, Braga, Sumur Bandung, Kota Bandung",
  stories: [
    { date: "2021", title: "Musim Dingin di Konya", body: "Dua mahasiswa beasiswa dari Indonesia bertemu di pengajian pelajar, lalu sama-sama tersesat mencari pasar kain tua." },
    { date: "2025", title: "Khitbah", body: "Sepulang studi, Fikri datang bersama keluarga ke Bandung untuk meminang Zahra dengan restu kedua orang tua." },
    { date: "2027", title: "Akad", body: "Dengan rahmat Allah, kami mulai menenun hari-hari sebagai suami dan istri." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Hotel Savoy Homann", address: "Jl. Asia Afrika No. 112, Braga, Sumur Bandung, Kota Bandung" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/a99.webp", "/themes/img/r58.webp", "/themes/img/a100.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 2044 31", account_name: "Zahra Aulia Nasution" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0217 5522 9", account_name: "Muhammad Fikri Ramadhan" },
    { id: "demo-kado", type: "address", address: "Jl. Tubagus Ismail VIII No. 21, Sekeloa, Coblong, Kota Bandung 40134" },
  ],
  guestName: "Ibu Hj. Fadhilah & Keluarga",
  guestTable: "Meja Kunyit 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Iringan nasyid & rebana" },
      { time: "11.30", title: "Kedatangan kedua mempelai" },
      { time: "12.00", title: "Jamuan", note: "Nasi kebuli, kebab, & teh apel" },
      { time: "13.15", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim bernuansa hangat: merah bata, nila, kunyit, atau krem.", colors: ["#a23a24", "#2a3263", "#d69a2c", "#ece0c3"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Irwan Nasution", "Kel. Besar Drs. H. Agus Salim", "Ikatan Alumni Pelajar Indonesia di Türkiye"] },
  },
});
