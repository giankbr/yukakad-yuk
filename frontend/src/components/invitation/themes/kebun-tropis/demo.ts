import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Fikri",
    brideFull: "Nadia Putri Ramadhani, S.Ds.", groomFull: "Muhammad Fikri Alamsyah, S.T.",
    brideParents: "Putri pertama dari\nBapak Hendra Wijaya & Ibu Sri Lestari", groomParents: "Putra ketiga dari\nBapak H. Ahmad Alamsyah & Ibu Hj. Rahmawati",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Tumbuh bersama seperti kebun kecil di halaman rumah: disiram sabar, disinari doa.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T08:00:00+07:00",
  place: "Taman Tropika Garden Venue",
  address: "Jl. Pajajaran No. 88, Baranangsiang, Bogor Timur, Kota Bogor",
  stories: [
    { date: "2021", title: "Pameran Tanaman", body: "Bertemu di pameran tanaman hias; Nadia mencari strelitzia, Fikri menjaga stan pembibitan milik pamannya." },
    { date: "2024", title: "Kebun Pertama", body: "Kami merawat kebun kecil di atap kos, belajar sabar menunggu kuncup yang tak kunjung mekar." },
    { date: "2027", title: "Musim Bersemi", body: "Dengan restu kedua keluarga, kami memulai rumah tangga di bawah langit yang cerah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Bantarjati, Bogor Utara, Kota Bogor" },
    { name: "Resepsi Taman", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Taman Tropika Garden Venue", address: "Jl. Pajajaran No. 88, Baranangsiang, Bogor Timur, Kota Bogor" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/r1.webp", "/themes/img/r13.webp", "/themes/img/r108.webp", "/themes/img/r16.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Nadia Putri Ramadhani" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 3456 7788", account_name: "M. Fikri Alamsyah" },
  ],
  guestName: "Ibu Ratna Sari & Keluarga",
  guestTable: "Meja 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan di taman", note: "Es kelapa muda & jajanan pasar" },
      { time: "11.30", title: "Kirab pengantin" },
      { time: "12.00", title: "Ramah tamah & makan siang" },
      { time: "13.15", title: "Foto bersama", note: "Di gerbang bunga" },
    ] },
    dressCode: { note: "Warna cerah ala taman tropis: koral, hijau daun, kuning matahari. Busana sopan & nyaman untuk acara luar ruang.", colors: ["#f26b4f", "#1f8a5b", "#f6c343", "#fff6e6"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-22T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Wijaya", "Kel. Besar Bpk. H. Ahmad Alamsyah"] },
  },
});
