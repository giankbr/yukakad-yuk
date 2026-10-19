import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Arya",
    note: "Seperti mawar yang mekar pada waktunya, cinta kami tumbuh perlahan dan akhirnya menemukan musimnya.",
    brideFull: "Kirana Ayu Larasati, S.Ds.", groomFull: "Arya Wicaksana Putra, S.T.",
    brideParents: "Putri kedua dari\nBapak Hadi Prasetyo & Ibu Ratih Kusumawati",
    groomParents: "Putra pertama dari\nBapak Bambang Wicaksono & Ibu Laras Sekarsari",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T09:00:00+07:00",
  place: "Grand Ballroom Hotel Padma",
  address: "Jl. Rancabentang No. 56-58, Ciumbuleuit, Bandung",
  stories: [
    { date: "2019", title: "Pertemuan Pertama", body: "Bertemu di pameran ilustrasi kampus. Arya membeli kartu pos mawar buatan Kirana, lalu kembali keesokan harinya untuk membeli satu lagi." },
    { date: "2022", title: "Merajut Cerita", body: "Tiga tahun bersahabat, saling menguatkan saat skripsi dan pekerjaan pertama, hingga sadar hati sudah memilih." },
    { date: "2026", title: "Lamaran", body: "Keluarga Arya datang ke rumah Kirana membawa seserahan dan sebuket mawar merah muda." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Bandung" },
    { name: "Resepsi", date: "2027-05-15T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "Grand Ballroom Hotel Padma", address: "Jl. Rancabentang No. 56-58, Ciumbuleuit, Bandung" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a18.webp", "/themes/img/r85.webp", "/themes/img/r13.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4370 2215 88", account_name: "Kirana Ayu Larasati" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0187 6543 2", account_name: "Arya Wicaksana Putra" },
    { id: "demo-kado", type: "address", address: "Jl. Sukajadi No. 128, Sukajadi, Bandung 40162" },
  ],
  guestName: "Ibu Sinta Maharani & Keluarga",
});
