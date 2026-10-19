import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alesha", groom: "Damar",
    brideFull: "Alesha Putri Maharani, S.E.", groomFull: "Damar Satria Wibisono, M.M.",
    brideParents: "Putri pertama dari\nBapak Ir. Hendra Gunawan & Ibu Sinta Maharani", groomParents: "Putra kedua dari\nBapak Bambang Wibisono & Ibu Ratna Kusuma",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Dua jiwa, satu janji, dan sebuah awal yang kami rayakan bersama orang-orang terkasih.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T10:00:00+07:00",
  place: "Grand Ballroom Kencana Tower",
  address: "Jl. Jend. Sudirman Kav. 52, Senayan, Jakarta Selatan",
  stories: [
    { date: "2019", title: "Pertemuan", body: "Bertemu di sebuah pameran seni rupa di Jakarta. Alesha memandangi lukisan yang sama terlalu lama, Damar memberanikan diri bertanya." },
    { date: "2022", title: "Melangkah Bersama", body: "Dari kopi akhir pekan hingga perjalanan pertama ke luar kota, keduanya belajar bahwa rumah bisa berupa seseorang." },
    { date: "2026", title: "Lamaran", body: "Di hadapan kedua keluarga, Damar menyematkan cincin sederhana yang dipilih bersama ibundanya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Masjid Al-Hikmah Kebayoran", address: "Jl. Hang Lekir I No. 8, Kebayoran Baru, Jakarta Selatan" },
    { name: "Resepsi", date: "2027-06-12T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Grand Ballroom Kencana Tower", address: "Jl. Jend. Sudirman Kav. 52, Senayan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a78.webp", "/themes/img/r88.webp", "/themes/img/a74.webp", "/themes/img/r75.webp", "/themes/img/a117.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0388 21", account_name: "Alesha Putri Maharani" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 8899 2027", account_name: "Damar Satria W." },
  ],
  guestName: "Bapak Andreas Kurniawan & Partner",
});
