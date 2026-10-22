import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Dimas",
    brideFull: "Kirana Larasati Wibowo", groomFull: "Dimas Prasetya Adinugroho",
    brideParents: "Putri pertama dari\nBapak Hendro Wibowo & Ibu Maria Sulistyowati", groomParents: "Putra kedua dari\nBapak Agus Adinugroho & Ibu Retno Palupi",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Kami pernah retak, lalu belajar menyatukan diri pelan-pelan. Bekasnya kami biarkan terlihat, karena di situlah cahayanya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T10:00:00+07:00",
  place: "Tirana House",
  address: "Jl. Suryodiningratan No. 7, Mantrijeron, Kota Yogyakarta",
  stories: [
    { date: "2020", title: "Satu Meja Putar", body: "Kami bertemu di kelas keramik akhir pekan di Kasongan. Mangkuk pertamaku miring, mangkuk pertamanya retak di tungku." },
    { date: "2023", title: "Jarak & Jeda", body: "Kerja di dua kota membuat kami sempat berhenti. Setahun kemudian kami sepakat memulai lagi, lebih jujur dan lebih sabar." },
    { date: "Mei 2027", title: "Lamaran", body: "Ia melamar dengan sebuah mangkuk yang ia perbaiki sendiri dengan garis emas: mangkuk pertamanya yang dulu retak itu." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-10-09T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Tirana House", address: "Jl. Suryodiningratan No. 7, Mantrijeron, Kota Yogyakarta" },
    { name: "Resepsi", date: "2027-10-09T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Greenhost Boutique Hotel", address: "Jl. Prawirotaman II No. 629, Brontokusuman, Mergangsan, Kota Yogyakarta" },
  ],
  gallery: ["/themes/img/r88.webp", "/themes/img/r1.webp", "/themes/img/r5.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4451 0927 33", account_name: "Kirana Larasati Wibowo" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1370 0188 2456 1", account_name: "Dimas Prasetya Adinugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Tirtodipuran No. 41, Mantrijeron, Kota Yogyakarta 55143", account_name: "Kirana & Dimas" },
  ],
  guestName: "Ibu Sekar Ayuningtyas & Keluarga",
  guestTable: "Meja Raku 3",
  extras: {
    quote: { text: "Cinta tidak membuat kita utuh tanpa cela. Cinta membuat kita mau saling memperbaiki, dan tidak malu pada bekasnya.", source: "Kirana & Dimas" },
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Keluarga inti & sahabat" },
      { time: "11.00", title: "Ramah tamah & teh sore", note: "Di taman belakang" },
      { time: "18.30", title: "Resepsi dibuka" },
      { time: "20.00", title: "Pemotongan kue & foto bersama" },
    ] },
    dressCode: { note: "Netral dan tenang: krem, abu arang, hitam, dengan sentuhan emas bila berkenan.", colors: ["#f2ede3", "#c9c1b3", "#2b2926", "#b98f3e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-09T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Hendro Wibowo", "Kel. Besar Agus Adinugroho", "Komunitas Keramik Kasongan"] },
    wishlist: { items: [
      { id: "w1", name: "Set peralatan teh keramik", price: "± Rp900.000" },
      { id: "w2", name: "Kelas keramik berdua", price: "± Rp650.000", claimed_by: "Sekar" },
      { id: "w3", name: "Tanaman untuk teras", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah upacara terbuka untuk semua tamu?", a: "Upacara pagi terbatas untuk keluarga dan sahabat dekat. Semua tamu kami nantikan di resepsi malam." },
      { q: "Apakah tersedia parkir?", a: "Parkir mobil tersedia di area Prawirotaman, kami sarankan menggunakan taksi daring." },
    ] },
  },
});
