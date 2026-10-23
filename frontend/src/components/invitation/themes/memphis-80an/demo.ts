import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Bastian",
    brideFull: "Sekar Ayu Larasati", groomFull: "Bastian Wicaksono",
    brideParents: "Putri dari\nBapak Hendra Gunawan & Ibu Ratna Dewi",
    groomParents: "Putra dari\nBapak Yohanes Wicaksono & Ibu Maria Lestari",
    bridePhoto: "/themes/img/r100.webp",
    groomPhoto: "/themes/img/r101.webp",
    note: "Satu suka warna pastel, satu suka hitam-putih. Ternyata kalau ditaruh berdampingan, jadinya pas sekali.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T15:00:00+07:00",
  place: "Studio Atap Kemang",
  address: "Jl. Kemang Raya No. 8, Bangka, Kec. Mampang Prapatan, Jakarta Selatan",
  story: { title: "Cerita Kami", body: "" },
  stories: [
    { date: "2021", title: "Satu meja di kelas tipografi", body: "Sekar datang terlambat dan hanya ada satu kursi kosong: di sebelah Bastian, yang sedang menggambar huruf-huruf aneh di pinggir buku catatannya." },
    { date: "2023", title: "Proyek poster bersama", body: "Kami mengerjakan poster festival musik berdua. Bertengkar soal warna, berdamai di depan semangkuk mi ayam, lalu sadar kami tim yang hebat." },
    { date: "2026", title: "Lamaran di pameran", body: "Di sela pameran desain kecil kami, Bastian menyelipkan satu poster tambahan bertuliskan: maukah kamu menikah denganku?" },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-09-18T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Studio Atap Kemang", address: "Jl. Kemang Raya No. 8, Bangka, Kec. Mampang Prapatan, Jakarta Selatan" },
    { name: "Pesta Resepsi", date: "2027-09-18T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Studio Atap Kemang, lantai 3", address: "Jl. Kemang Raya No. 8, Bangka, Kec. Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a123.webp", "/themes/img/a112.webp", "/themes/img/r63.webp", "/themes/img/r103.webp", "/themes/img/r75.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0918 33", account_name: "Sekar Ayu Larasati" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 8890 1127", account_name: "Bastian Wicaksono" },
  ],
  guestName: "Mas Rendy & Partner",
  guestTable: "Meja Zigzag 7",
  extras: {
    quote: { text: "Cinta itu seperti desain yang baik: tidak berteriak, tapi membuat segalanya terasa pada tempatnya.", source: "Catatan kecil kami" },
    rundown: { items: [
      { time: "15.00", title: "Upacara pernikahan", note: "Mohon hadir 15 menit lebih awal" },
      { time: "16.00", title: "Foto bersama & kudapan sore" },
      { time: "18.30", title: "Pesta resepsi dibuka", note: "Makan malam & musik" },
      { time: "20.30", title: "Lantai dansa", note: "Lagu-lagu 80-an, siapkan gerakan terbaik" },
    ] },
    dressCode: { note: "Warna-warni pastel, motif berani, atau hitam-putih. Gaya 80-an sangat dianjurkan.", colors: ["#f7a8c4", "#8fdcc2", "#b9a5ef", "#ffd54a", "#151515"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Ada area parkir?", a: "Ada parkir terbatas di basement. Kami sarankan memakai transportasi daring." },
      { q: "Boleh membawa anak?", a: "Boleh, ada sudut menggambar kecil untuk anak-anak di lantai 2." },
    ] },
  },
});
