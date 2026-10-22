import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Clara", groom: "Yohan",
    brideFull: "Clara Wulandari Putri, S.Ds.", groomFull: "Yohanes Bramantyo Nugroho, S.Sn.",
    brideParents: "Putri kedua dari\nBapak Fransiskus Hadi Wibowo & Ibu Maria Retno Sulistyani",
    groomParents: "Putra sulung dari\nBapak Paulus Agung Nugroho & Ibu Veronika Endah Lestari",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Dua potongan kertas yang berbeda warna, ternyata paling pas kalau ditempel berdampingan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T10:00:00+07:00",
  place: "Pendopo Omah Kebun Kaliurang",
  address: "Jl. Kaliurang Km. 17,5, Pakembinangun, Pakem, Sleman, Yogyakarta",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Lokakarya zine", body: "Kami duduk bersebelahan di lokakarya membuat zine di Kotabaru. Clara kehabisan lem, Yohan meminjamkan gunting dan lemnya sekaligus." },
    { date: "2021", title: "Pameran kecil", body: "Kolase pertama yang kami kerjakan berdua dipajang di sebuah kedai kopi. Tidak laku, tapi kami jadi sering bertemu." },
    { date: "2026", title: "Lamaran di studio", body: "Di antara tumpukan kertas warna, Yohan menyembunyikan cincin di balik potongan bintang kuning." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-05-15T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gereja Kristen Jawa Gondokusuman", address: "Jl. Dr. Wahidin Sudirohusodo No. 30, Kotabaru, Gondokusuman, Yogyakarta" },
    { name: "Resepsi Taman", date: "2027-05-15T16:00:00+07:00", time: "16.00 – 19.00 WIB", venue: "Pendopo Omah Kebun Kaliurang", address: "Jl. Kaliurang Km. 17,5, Pakembinangun, Pakem, Sleman, Yogyakarta" },
  ],
  gallery: ["/themes/img/r103.webp", "/themes/img/a95.webp", "/themes/img/r85.webp", "/themes/img/a101.webp", "/themes/img/r100.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "4560 1187 22", account_name: "Clara Wulandari Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Cendana No. 14, Semaki, Umbulharjo, Yogyakarta 55166" },
  ],
  guestName: "Mbak Ayu Kirana & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati; ia tidak cemburu. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu.", source: "1 Korintus 13:4, 7" },
    rundown: { items: [
      { time: "10.00", title: "Ibadah pemberkatan", note: "Keluarga & sahabat" },
      { time: "16.00", title: "Resepsi taman dibuka", note: "Musik akustik & jajanan pasar" },
      { time: "17.00", title: "Pojok kolase bersama", note: "Tempel ucapanmu di papan kenangan" },
      { time: "18.15", title: "Potong kue & foto bersama" },
    ] },
    dressCode: { note: "Berani warna! Pilih satu warna cerah favoritmu, motif bebas.", colors: ["#e4512f", "#2f4fb8", "#f2b52e", "#2f8a57", "#f3a7b4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Hadi Wibowo", "Keluarga Besar Agung Nugroho", "Teman-teman Komunitas Zine Jogja"] },
    wishlist: { note: "Kehadiran kalian sudah cukup. Kalau ingin memberi, ini yang sedang kami kumpulkan untuk rumah baru.", items: [
      { id: "w1", name: "Pemotong kertas meja", price: "± Rp650.000" },
      { id: "w2", name: "Set pot tanaman gerabah", price: "± Rp300.000", claimed_by: "Dinda" },
      { id: "w3", name: "Voucher toko buku", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah ada parkir?", a: "Ada, di halaman Omah Kebun. Dari gereja ke lokasi resepsi sekitar 35 menit berkendara." },
      { q: "Boleh membawa anak?", a: "Tentu! Ada meja mewarnai dan kertas tempel untuk tamu kecil." },
    ] },
  },
});
