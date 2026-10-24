import { makeDemo } from "../demo-base";

// Ulang tahun anak bertema pesta kostum: topeng kertas, jubah, mahkota, rak baju dandan, dan panggung kecil di Sleman.
export const demo = makeDemo({
  couple: {
    bride: "Gendis", groom: "",
    brideFull: "Gendis Ayu Pramesti",
    brideParents: "Putri pertama dari Bapak Raditya Pramono & Ibu Ayu Larasati",
    note: "Gendis ingin semua teman datang memakai kostum buatan sendiri: jubah dari kain bekas, mahkota karton, atau topeng kertas. Yang penting seru dan percaya diri!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-05-22T15:00:00+07:00",
  place: "Aula Taman Bermain Kayu Manis",
  address: "Jl. Kaliurang Km. 7, Sinduharjo, Ngaglik, Kabupaten Sleman, DI Yogyakarta",
  story: { title: "Lemari Kostum Gendis", body: "" },
  stories: [
    { date: "2021", title: "Lahir di bulan Mei", body: "Gendis lahir saat pohon flamboyan di depan rumah sedang merah-merahnya." },
    { date: "2024", title: "Jubah pertama", body: "Sarung Ayah diikat di leher jadi jubah, dan sejak itu Gendis selalu ingin 'terbang' keliling ruang tamu." },
    { date: "2026", title: "Panggung TK", body: "Tampil sebagai kucing ungu di pentas TK, dengan topeng kertas yang ia gunting sendiri." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang ingin mengajak semua teman berdandan bersama dan naik ke panggung kecil." },
  ],
  events: [
    { name: "Pesta Kostum Gendis", date: "2027-05-22T15:00:00+07:00", time: "15.00 – 18.00 WIB", venue: "Aula Taman Bermain Kayu Manis", address: "Jl. Kaliurang Km. 7, Sinduharjo, Ngaglik, Kabupaten Sleman, DI Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0817 2245 63", account_name: "Ayu Larasati" },
    { id: "demo-kado", type: "address", address: "Perum Griya Kaliurang Blok C-12, Sardonoharjo, Ngaglik, Sleman 55581" },
  ],
  guestName: "Adik Bima & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Gendis Ayu Pramesti", nickname: "Gendis", birthDate: "2021-05-22T06:40:00+07:00", parents: "Putri pertama dari Bapak Raditya Pramono & Ibu Ayu Larasati" },
    quote: { text: "Hari ini boleh jadi raja, ksatria, peri, atau kucing ungu. Yang paling penting, tetap jadi teman yang baik.", source: "Ayah & Bunda" },
    rundown: { items: [
      { time: "15.00", title: "Pojok dandan", note: "Rak kostum, mahkota karton, dan cat wajah tersedia untuk yang belum berkostum" },
      { time: "15.45", title: "Parade kostum di panggung kecil", note: "Semua anak dapat medali kertas" },
      { time: "16.30", title: "Membuat topeng kertas bersama" },
      { time: "17.15", title: "Tiup lilin & makan kue" },
    ] },
    dressCode: { note: "Wajib berkostum! Boleh buatan sendiri: jubah, mahkota, topeng, sayap, atau baju hewan favorit.", colors: ["#ef5b3f", "#ffc53a", "#1f9e9a", "#7a4fb5"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Pramono", "Eyang Kakung & Uti Larasati"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Gendis.", items: [
      { id: "w1", name: "Set kertas lipat & gunting anak", price: "± Rp85.000" },
      { id: "w2", name: "Buku cerita bergambar", price: "± Rp95.000", claimed_by: "Tante Rini" },
      { id: "w3", name: "Kostum hewan (ukuran 6–7 tahun)", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Belum punya kostum, boleh datang?", a: "Boleh sekali! Ada pojok dandan dengan rak kostum dan mahkota karton." },
      { q: "Apakah orang tua boleh ikut berkostum?", a: "Sangat boleh, makin ramai makin seru." },
    ] },
  },
});
