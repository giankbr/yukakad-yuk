import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alana", groom: "Raditya",
    note: "Dua jiwa, satu janji, dan malam yang akan selalu kami kenang.",
    brideFull: "Alana Prameswari, M.M.", groomFull: "Raditya Mahendra Kusuma, S.E.",
    brideParents: "Putri dari\nBapak Irawan Santoso & Ibu Melinda Hartati",
    groomParents: "Putra dari\nBapak Surya Kusuma & Ibu Diana Puspita",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T18:30:00+07:00",
  place: "The Dharmawangsa Jakarta",
  address: "Jl. Brawijaya Raya No. 26, Kebayoran Baru, Jakarta Selatan",
  stories: [
    { date: "2018", title: "Sebuah Pesta Dansa", body: "Bertemu di malam gala amal. Raditya salah mengambil gelas Alana, lalu meminta maaf dengan satu dansa." },
    { date: "2021", title: "Kota yang Sama", body: "Pindah kerja ke Jakarta di tahun yang sama. Makan malam Jumat menjadi tradisi berdua." },
    { date: "2026", title: "Sebuah Cincin", body: "Di rooftop tempat mereka pertama kali berdansa, Raditya berlutut dan Alana menjawab ya." },
  ],
  events: [
    { name: "Pemberkatan & Akad", date: "2027-09-18T15:00:00+07:00", time: "15.00 – 16.30 WIB", venue: "Ballroom Nusantara", address: "The Dharmawangsa, Jl. Brawijaya Raya No. 26, Jakarta Selatan" },
    { name: "Resepsi Malam", date: "2027-09-18T18:30:00+07:00", time: "18.30 – 22.00 WIB", venue: "The Dharmawangsa Jakarta", address: "Jl. Brawijaya Raya No. 26, Kebayoran Baru, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a86.webp", "/themes/img/a87.webp", "/themes/img/a85.webp", "/themes/img/a83.webp", "/themes/img/a40.webp", "/themes/img/a84.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0098 32", account_name: "Alana Prameswari" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 8899 2026", account_name: "Raditya Mahendra" },
    { id: "demo-kado", type: "address", address: "Apartemen Senayan Residence Tower 2 Unit 18B, Jl. Patal Senayan No. 1, Jakarta Selatan" },
  ],
  guestName: "Bapak Haryo Wibisono & Partner",
});
