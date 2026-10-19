import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Rayhan",
    note: "Semoga ikatan ini menjadi ladang pahala dan awal dari kebaikan yang tak berkesudahan.",
    brideFull: "Nadia Syakira Rahmani, S.H.", groomFull: "Rayhan Akbar Maulana, S.E.",
    brideParents: "Putri dari Bapak H. Syamsul Bahri & Ibu Hj. Rahmawati",
    groomParents: "Putra dari Bapak H. Iskandar Muda & Ibu Hj. Cut Aminah",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Masjid Raya Baiturrahman",
  address: "Jl. Moh. Jam No. 1, Banda Aceh",
  stories: [
    { title: "Pertemuan", date: "2022", body: "Bertemu di sebuah forum mahasiswa di Medan, berawal dari diskusi panjang tentang buku." },
    { title: "Ta'aruf", date: "2025", body: "Dengan perantara keluarga, kami berta'aruf dan saling memantapkan niat." },
    { title: "Meminang", date: "Januari 2027", body: "Rayhan dan keluarga datang membawa seserahan, disambut dengan ranub lampuan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Raya Baiturrahman", address: "Jl. Moh. Jam No. 1, Banda Aceh" },
    { name: "Resepsi Pernikahan", date: "2027-07-11T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Hermes Palace Hotel — Grand Ballroom", address: "Jl. T. Panglima Nyak Makam, Banda Aceh" },
  ],
  gallery: ["/themes/img/a118.webp", "/themes/img/a85.webp", "/themes/img/r65.webp", "/themes/img/a116.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Aceh Syariah", account_number: "01002345678", account_name: "Nadia Syakira Rahmani" },
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7134567890", account_name: "Rayhan Akbar Maulana" },
  ],
  guestName: "Bapak Teuku Hasan & Keluarga",
});
