import { makeDemo } from "../demo-base";

// Pernikahan romantis di taman mawar Kota Batu: upacara sore di taman dan resepsi malam di rumah kaca.
export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Dimas",
    brideFull: "Alya Prameswari Hadinata", groomFull: "Dimas Arya Wicaksana",
    brideParents: "Putri sulung dari\nBapak Hendra Hadinata & Ibu Ratna Kusumawati", groomParents: "Putra kedua dari\nBapak Agus Wicaksono & Ibu Lestari Pertiwi",
    note: "Mawar yang mekar paling indah adalah yang dirawat setiap hari. Begitulah kami ingin saling menjaga.",
  },
  eventLabel: "Pernikahan",
  date: "2027-02-13T15:00:00+07:00",
  place: "Taman Mawar Kusuma",
  address: "Jl. Raya Selecta No. 18, Tulungrejo, Kec. Bumiaji, Kota Batu, Jawa Timur",
  stories: [
    { date: "2020", title: "Satu Kelas Melukis", body: "Kami bertemu di kelas melukis akhir pekan di Malang. Alya melukis mawar, Dimas melukis vas yang selalu miring." },
    { date: "2023", title: "Kebun di Atap", body: "Kami menanam sebelas pot mawar di atap kos Dimas. Sebagian layu, tetapi yang bertahan mekar merah tua setiap musim hujan." },
    { date: "2026", title: "Setangkai untuk Selamanya", body: "Di bawah pergola mawar, Dimas melamar dengan setangkai mawar merah dan cincin yang diikat pita. Jawabannya: ya." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-02-13T15:00:00+07:00", time: "15.00 – 16.30 WIB", venue: "Taman Mawar Kusuma", address: "Jl. Raya Selecta No. 18, Tulungrejo, Kec. Bumiaji, Kota Batu" },
    { name: "Resepsi", date: "2027-02-13T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Rumah Kaca Kusuma", address: "Kompleks Taman Mawar Kusuma, Jl. Raya Selecta No. 18, Kota Batu" },
  ],
  gallery: ["/themes/img/a31.webp", "/themes/img/a26.webp", "/themes/img/r5.webp", "/themes/img/r109.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "3150 2130 27", account_name: "Alya Prameswari Hadinata" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "144 00 2713 0227", account_name: "Dimas Arya Wicaksana" },
    { id: "demo-kado", type: "address", address: "Jl. Bunga Mawar No. 9, Lowokwaru, Kota Malang 65141" },
  ],
  guestName: "Ibu Sinta Maharani & Keluarga",
  guestTable: "Mawar 3",
  extras: {
    quote: { text: "Cinta tidak saling memandang, tetapi bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Minuman hangat di pergola mawar" },
      { time: "19.00", title: "Masuknya kedua mempelai" },
      { time: "19.30", title: "Makan malam & musik akustik" },
      { time: "21.00", title: "Dansa pertama & potong kue" },
    ] },
    dressCode: { note: "Nuansa merah tua, krem, dan hijau daun. Hindari putih polos.", colors: ["#7a1420", "#f6ecdc", "#2f3b28", "#c8403f"] },
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Kel. Besar Hadinata", "Kel. Besar Wicaksono", "Sahabat Kelas Melukis Sabtu"] },
  },
});
