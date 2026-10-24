import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tari", groom: "Yudha",
    brideFull: "Lestari Ayu Ningtyas", groomFull: "Yudha Pratama Wicaksono",
    brideParents: "Putri bungsu dari\nBapak Slamet Riyadi & Ibu Endang Puspitasari",
    groomParents: "Putra pertama dari\nBapak Hari Wicaksono & Ibu Tutik Handayani",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Kami bertemu di musim petik, dan sejak itu setiap musim terasa manis. Datang, bawa keranjangmu, mari panen bahagia bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Kebun Apel Lereng Panderman",
  address: "Jl. Raya Oro-oro Ombo, Temas, Kecamatan Batu, Kota Batu",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2020", title: "Musim Petik Pertama", body: "Tari memandu rombongan wisata petik apel, Yudha salah satu tamunya. Keranjangnya penuh, tapi yang dia ingat cuma senyum pemandunya." },
    { date: "2023", title: "Bolak-balik Malang–Batu", body: "Setiap Minggu Yudha naik ke Batu, katanya mau beli apel. Lama-lama warung keluarga Tari hafal pesanannya." },
    { date: "2026", title: "Di Bawah Pohon Rome Beauty", body: "Di pohon apel tertua di kebun, Yudha menyembunyikan cincin di dalam keranjang. Tari menemukannya di antara apel merah." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Pendopo Kebun Apel Lereng Panderman", address: "Jl. Raya Oro-oro Ombo, Temas, Kecamatan Batu, Kota Batu" },
    { name: "Resepsi di Kebun", date: "2027-07-10T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Taman Petik Blok C", address: "Kebun Apel Lereng Panderman, Jl. Raya Oro-oro Ombo, Kota Batu" },
  ],
  gallery: ["/themes/img/r1.webp", "/themes/img/r16.webp", "/themes/img/r81.webp", "/themes/img/r75.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0071 0100 4521 509", account_name: "Lestari Ayu Ningtyas" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 3344 5566", account_name: "Yudha Pratama Wicaksono" },
    { id: "demo-kado", type: "address", address: "Jl. Bukit Berbunga No. 41, Sidomulyo, Kota Batu 65317" },
  ],
  guestName: "Mas Bayu & Partner",
  guestTable: "Meja Rome Beauty",
  extras: {
    quote: { text: "Cinta itu seperti kebun: tidak tumbuh dalam semalam, tapi kalau dirawat setiap hari, ia berbuah pada musimnya.", source: "Tari & Yudha" },
    rundown: { items: [
      { time: "09.00", title: "Upacara pernikahan", note: "Pendopo kebun" },
      { time: "11.00", title: "Resepsi & makan siang", note: "Prasmanan khas Batu" },
      { time: "13.00", title: "Petik apel bersama", note: "Setiap tamu dapat satu keranjang" },
      { time: "14.30", title: "Foto bersama di kebun" },
    ] },
    dressCode: { note: "Santai rapi bernuansa kebun: merah apel, hijau daun, krem, dan cokelat kayu. Pakai alas kaki datar, acara di atas rumput.", colors: ["#c92a33", "#4f8a3a", "#fbf1dc", "#b07a45"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak Slamet Riyadi", "Kel. Besar Bapak Hari Wicaksono", "Kelompok Tani Apel Sumber Rejeki"] },
    travel: { note: "Kota Batu sejuk, suhu siang ± 20°C. Akses dari Malang ± 45 menit.", items: [
      { name: "Parkir", detail: "Area parkir kebun, dilanjutkan mobil wisata ke Blok C" },
      { name: "Penginapan", detail: "Banyak villa dan homestay di Jl. Oro-oro Ombo, ± 5 menit" },
    ] },
  },
});
