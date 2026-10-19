import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Arya",
    brideFull: "Kirana Sekar Ayu, S.Hum.", groomFull: "Arya Wicaksana, S.T.",
    brideParents: "Putri kedua dari\nBapak Haryo Sasongko & Ibu Dewi Kartika", groomParents: "Putra sulung dari\nBapak Darmawan Prasetyo & Ibu Lestari Ningsih",
    bridePhoto: "/themes/img/r53.webp", groomPhoto: "/themes/img/r52.webp",
    note: "Dari sepucuk surat, tumbuh cerita yang kini kami tulis bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T09:00:00+07:00",
  place: "Rumah Heritage Dago",
  address: "Jl. Ir. H. Juanda No. 88, Dago, Bandung",
  stories: [
    { date: "2016", title: "Sahabat Pena", body: "Berkenalan lewat program surat-menyurat antarkota. Kirana di Bandung, Arya di Semarang, dan tukang pos yang selalu jadi perantara." },
    { date: "2019", title: "Bertemu di Braga", body: "Tiga tahun bertukar surat, akhirnya bertemu di sebuah toko buku tua. Keduanya datang membawa surat terakhir sebagai tanda pengenal." },
    { date: "2026", title: "Surat Lamaran", body: "Keluarga Arya datang ke rumah dengan sepucuk surat lamaran bertulis tangan, disegel lilin merah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Jami' Cipaganti", address: "Jl. R.A.A. Wiranatakusumah No. 85, Cipaganti, Bandung" },
    { name: "Resepsi", date: "2027-05-15T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Rumah Heritage Dago", address: "Jl. Ir. H. Juanda No. 88, Dago, Bandung" },
  ],
  gallery: ["/themes/img/r55.webp", "/themes/img/a31.webp", "/themes/img/r56.webp", "/themes/img/r54.webp", "/themes/img/r51.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0812 3456 78", account_name: "Kirana Sekar Ayu" },
    { id: "demo-kado", type: "address", address: "Jl. Cihampelas No. 41, Cipaganti, Coblong, Bandung 40131" },
  ],
  guestName: "Ibu Ratih Purnamasari & Keluarga",
});
