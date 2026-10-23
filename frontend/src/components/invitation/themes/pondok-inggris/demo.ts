import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Bastian",
    brideFull: "Kirana Laksmi Pratiwi, S.Ars.", groomFull: "Bastian Adiwangsa Putra, S.P.",
    brideParents: "Putri pertama dari\nBapak Hadi Prasetyo & Ibu Ratna Wulandari", groomParents: "Putra kedua dari\nBapak Agus Adiwangsa & Ibu Lestari Handayani",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Sebuah pondok kecil, kebun yang tak pernah selesai ditanami, dan kami berdua yang belajar merawatnya setiap pagi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T15:00:00+07:00",
  place: "Kebun Rosewood, Lembang",
  address: "Jl. Kolonel Masturi No. 147, Cikahuripan, Lembang, Kabupaten Bandung Barat",
  stories: [
    { date: "April 2021", title: "Pameran Bunga di Kebun Raya", body: "Kirana sedang menggambar sekuntum delphinium ketika Bastian, yang menjaga stan bibit, bertanya apakah gambar itu dijual. Tidak dijual, tapi nomor telepon akhirnya ditukar." },
    { date: "2023", title: "Pondok Pertama", body: "Kami menyewa pondok mungil di Lembang. Kirana merancang jendelanya, Bastian menanam mawar rambat yang kini sudah menutupi pintu." },
    { date: "Februari 2027", title: "Lamaran di Gerbang Kayu", body: "Bastian mengecat ulang gerbang pagar putih kami, lalu menunggu di sana dengan cincin dan seikat foxglove." },
  ],
  events: [
    { name: "Ikrar Pernikahan", date: "2027-05-15T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Paviliun Mawar, Kebun Rosewood", address: "Jl. Kolonel Masturi No. 147, Cikahuripan, Lembang, Kabupaten Bandung Barat" },
    { name: "Jamuan Teh & Resepsi Kebun", date: "2027-05-15T16:30:00+07:00", time: "16.30 – 20.00 WIB", venue: "Halaman Pondok, Kebun Rosewood", address: "Jl. Kolonel Masturi No. 147, Cikahuripan, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/r1.webp", "/themes/img/r75.webp", "/themes/img/r16.webp", "/themes/img/r84.webp", "/themes/img/r108.webp", "/themes/img/r8.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2310 7788 41", account_name: "Kirana Laksmi Pratiwi" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0192 4466 8", account_name: "Bastian Adiwangsa Putra" },
    { id: "demo-kado", type: "address", address: "Jl. Peneropongan Bintang No. 12, Gudangkahuripan, Lembang, Kabupaten Bandung Barat 40391" },
  ],
  guestName: "Ibu Margaretha Sinaga & Keluarga",
  guestTable: "Meja Foxglove 3",
  extras: {
    quote: { text: "Cinta itu seperti kebun: tidak pernah benar-benar selesai. Ia hanya perlu disiram setiap hari, dipangkas dengan sabar, dan dinikmati bersama ketika bunganya mekar.", source: "Catatan kebun Kirana & Bastian" },
    rundown: { items: [
      { time: "16.30", title: "Teh sore, scone & musik gesek", note: "Halaman depan pondok" },
      { time: "17.15", title: "Kedua mempelai menyapa tamu" },
      { time: "18.00", title: "Makan malam di bawah lampu taman" },
      { time: "19.15", title: "Potong kue & dansa pertama" },
    ] },
    dressCode: { note: "Pesta kebun sore hari: warna bunga musim semi, linen, dan sepatu yang nyaman di rumput.", colors: ["#d98a9a", "#a9bde8", "#c07fb0", "#a9bf93", "#f6efe0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hadi Prasetyo", "Kel. Besar Bpk. Agus Adiwangsa"] },
    travel: { note: "Udara Lembang sore hari cukup sejuk, bawalah selendang atau jaket tipis.", items: [
      { name: "Parkir", detail: "Area parkir kebun, ± 2 menit berjalan ke pondok" },
      { name: "Menginap", detail: "Penginapan di sekitar Jl. Raya Lembang, ± 10 menit berkendara" },
    ] },
  },
});
