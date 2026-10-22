import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Raditya",
    brideFull: "Alya Kirana Putri, S.Ds.", groomFull: "Raditya Pramana Wicaksono, S.Ars.",
    brideParents: "Putri pertama dari\nBapak H. Bambang Sudarsono & Ibu Hj. Ratna Kusumastuti", groomParents: "Putra kedua dari\nBapak Ir. Teguh Wicaksono & Ibu Dewi Anggraini",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Dua garis canting yang berbeda, kini bertemu dalam satu kain.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T08:00:00+07:00",
  place: "Gedung Arsip Nasional",
  address: "Jl. Gajah Mada No. 111, Krukut, Taman Sari, Jakarta Barat",
  stories: [
    { date: "2018", title: "Kelas Membatik", body: "Kami bertemu di kelas membatik akhir pekan di Kemang. Alya sudah mahir memegang canting, Raditya baru belajar meniup malam panas." },
    { date: "2021", title: "Pameran Pertama", body: "Raditya merancang ruang pameran untuk koleksi batik Alya. Sejak itu kami tak pernah berhenti berkarya bersama." },
    { date: "2026", title: "Selembar Kain", body: "Raditya melamar dengan selembar kain parang yang ia batik sendiri, lengkap dengan retakan malam yang tidak sempurna." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Cut Meutia", address: "Jl. Taman Cut Mutiah No. 1, Gondangdia, Menteng, Jakarta Pusat" },
    { name: "Resepsi", date: "2027-09-18T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Gedung Arsip Nasional", address: "Jl. Gajah Mada No. 111, Krukut, Taman Sari, Jakarta Barat" },
  ],
  gallery: ["/themes/img/r0.webp", "/themes/img/a28.webp", "/themes/img/a123.webp", "/themes/img/a29.webp", "/themes/img/a122.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 3456 78", account_name: "Alya Kirana Putri" },
    { id: "demo-wallet", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 9876 5432", account_name: "Raditya Pramana" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Timur Raya No. 45, Bangka, Mampang Prapatan, Jakarta Selatan 12730" },
  ],
  guestName: "Bapak Hendra Gunawan & Keluarga",
  guestTable: "Meja Kawung 7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.00", title: "Penyambutan tamu", note: "Lobi utama, galeri kain batik kontemporer" },
      { time: "19.30", title: "Kirab pengantin", note: "Diiringi gamelan aransemen modern" },
      { time: "20.00", title: "Makan malam & ramah tamah" },
      { time: "21.00", title: "Foto bersama", note: "Per rombongan" },
    ] },
    dressCode: { note: "Batik dengan warna berani sangat dianjurkan. Kobalt, jingga dan hijau mint akan serasi dengan dekorasi.", colors: ["#2340b8", "#f2762e", "#9fe3c8", "#121a3a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Bambang Sudarsono", "Kel. Besar Ir. Teguh Wicaksono", "Sanggar Batik Canting Kemang"] },
    travel: { note: "Untuk tamu dari luar kota, berikut pilihan terdekat dari lokasi resepsi.", items: [
      { name: "Hotel di kawasan Gajah Mada", detail: "± 1 km dari Gedung Arsip Nasional" },
      { name: "Parkir & transportasi", detail: "Parkir terbatas di halaman gedung; TransJakarta halte Olimo 3 menit berjalan kaki" },
    ] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Tentu, anak-anak sangat diterima." },
      { q: "Apakah wajib berbatik?", a: "Tidak wajib, tetapi kami senang sekali bila Anda mengenakan batik." },
    ] },
  },
});
