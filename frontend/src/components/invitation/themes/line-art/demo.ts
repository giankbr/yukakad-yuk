import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Raka",
    brideFull: "Alya Pramesti Hartanto", groomFull: "Raka Adinata Wibisono",
    brideParents: "Putri dari Bapak Hartanto Gunawan & Ibu Melinda Sari", groomParents: "Putra dari Bapak Yohanes Wibisono & Ibu Ratna Dewi",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Satu garis yang tidak pernah terputus: dari sapaan pertama sampai janji hari ini.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T10:00:00+07:00",
  place: "Galeri Ruang Putih",
  address: "Jl. Kemang Selatan VIII No. 21, Bangka, Mampang Prapatan, Jakarta Selatan",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Kelas Gambar Hari Minggu", body: "Alya mengajar kelas sketsa di sebuah galeri kecil. Raka datang sebagai murid yang tidak pernah bisa menggambar garis lurus." },
    { date: "2022", title: "Pameran Pertama", body: "Raka membantu memasang pameran tunggal Alya. Sejak malam itu, setiap karya selalu punya dua nama di belakangnya." },
    { date: "2026", title: "Satu Pertanyaan", body: "Di halaman terakhir buku sketsanya, Raka menggambar dua garis yang bertemu, lalu bertanya. Alya menjawab ya." },
  ],
  events: [
    { name: "Janji Pernikahan", date: "2027-09-18T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Galeri Ruang Putih", address: "Jl. Kemang Selatan VIII No. 21, Bangka, Mampang Prapatan, Jakarta Selatan" },
    { name: "Resepsi Taman", date: "2027-09-18T17:00:00+07:00", time: "17.00 – 21.00 WIB", venue: "Taman Belakang Ruang Putih", address: "Jl. Kemang Selatan VIII No. 21, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a74.webp", "/themes/img/a30.webp", "/themes/img/a31.webp", "/themes/img/r12.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0388 19", account_name: "Alya Pramesti Hartanto" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Selatan VIII No. 21, Jakarta Selatan 12730 (a.n. Alya & Raka)" },
  ],
  guestName: "Kak Nadine & Partner",
  guestTable: "Meja 7",
  extras: {
    quote: { text: "Cinta tidak saling memandang, tetapi bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "17.00", title: "Tamu datang", note: "Minuman sambutan di taman" },
      { time: "18.00", title: "Makan malam bersama" },
      { time: "19.30", title: "Dansa pertama" },
      { time: "20.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Hitam, putih, atau satu sentuhan biru kobalt.", colors: ["#1d1b19", "#faf8f3", "#3150c4", "#b9b4ac"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    wishlist: { items: [
      { id: "w1", name: "Set cat air profesional", price: "± Rp900.000" },
      { id: "w2", name: "Lampu gantung rotan", price: "± Rp650.000", claimed_by: "Sekar" },
      { id: "w3", name: "Tiket pameran di Yogyakarta", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah ada aturan berpakaian?", a: "Hitam, putih, atau satu aksen biru. Sepatu nyaman dianjurkan karena resepsi di taman berumput." },
      { q: "Boleh membawa anak?", a: "Boleh. Kami menyiapkan sudut menggambar kecil untuk tamu cilik." },
    ] },
  },
});
