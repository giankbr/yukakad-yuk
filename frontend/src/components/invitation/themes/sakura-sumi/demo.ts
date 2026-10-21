import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hana", groom: "Yudha",
    brideFull: "Hana Pertiwi Maharani, S.Si.", groomFull: "Yudha Prasetya Wardhana, S.Hut.",
    brideParents: "Putri bungsu dari\nBapak H. Slamet Riyadi & Ibu Hj. Nur Aini", groomParents: "Putra kedua dari\nBapak Ir. Bambang Wardhana & Ibu Ratna Sari",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti sakura di Cibodas: mekar sebentar setiap musim, tapi pohonnya tumbuh seumur hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-10T08:00:00+07:00",
  place: "Kebun Raya Cibodas",
  address: "Jl. Kebun Raya Cibodas, Sindanglaya, Cipanas, Kabupaten Cianjur, Jawa Barat",
  stories: [
    { date: "Maret 2020", title: "Di bawah pohon sakura", body: "Hana meneliti tanaman di kebun raya, Yudha tersesat mencari jalur ke air terjun. Kami berbagi payung saat hujan turun." },
    { date: "2023", title: "Musim demi musim", body: "Setiap tahun kami kembali saat sakura Cibodas mekar, menulis harapan baru di buku kecil yang sama." },
    { date: "2027", title: "Mekar bersama", body: "Kami memilih musim bunga untuk memulai hidup bersama, di tempat semuanya bermula." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-10T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Cianjur", address: "Jl. Siti Jenab, Pamoyanan, Cianjur, Kabupaten Cianjur" },
    { name: "Walimatul 'Urs", date: "2027-04-10T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Kebun Raya Cibodas", address: "Jl. Kebun Raya Cibodas, Sindanglaya, Cipanas, Kabupaten Cianjur" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Hana Pertiwi Maharani" },
    { id: "demo-kado", type: "address", address: "Jl. Raya Cipanas No. 21, Sindanglaya, Cipanas, Cianjur 43253" },
  ],
  guestName: "Ibu Dr. Laksmi Widyaningrum",
  guestTable: "Meja Sakura 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Taman Sakura" },
      { time: "11.30", title: "Kirab pengantin" },
      { time: "12.00", title: "Ramah tamah" },
    ] },
    dressCode: { note: "Nuansa lembut: putih gading, merah muda sakura, dan abu tinta.", colors: ["#f4efe4", "#f4ccd3", "#8d867f", "#1d1a18"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Slamet Riyadi", "Kel. Besar Ir. Bambang Wardhana"] },
  },
});
