import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nayla", groom: "Raka",
    brideFull: "Nayla Kinanti Sasmita, S.Sn.", groomFull: "Raka Adiputra Nugraha, S.P.",
    brideParents: "Putri tunggal dari\nBapak Agus Sasmita & Ibu Rini Wulandari", groomParents: "Putra ketiga dari\nBapak H. Slamet Nugraha & Ibu Hj. Sri Wahyuni",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Di bawah langit sore dan semilir rumput ilalang, kami memulai perjalanan baru.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T08:30:00+07:00",
  place: "Kebun Joglo Tegal Sari",
  address: "Jl. Kaliurang Km. 17, Pakem, Sleman, Yogyakarta",
  stories: [
    { date: "2017", title: "Kelas Keramik", body: "Bertemu di kelas membuat gerabah di Kasongan. Tangan penuh tanah liat, tawa yang tak berhenti." },
    { date: "2020", title: "Menanam Bersama", body: "Raka mengajak Nayla menanam kebun kecil di halaman rumah. Dari situ mereka belajar sabar menunggu yang tumbuh." },
    { date: "2026", title: "Lamaran Sederhana", body: "Di sebuah piknik sore di lereng Merapi, keluarga berkumpul dan dua hati resmi diikat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-21T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Al-Ikhlas Pakem", address: "Jl. Kaliurang Km. 17,5, Pakem, Sleman, Yogyakarta" },
    { name: "Garden Party", date: "2027-08-21T15:30:00+07:00", time: "15.30 – 18.30 WIB", venue: "Kebun Joglo Tegal Sari", address: "Jl. Kaliurang Km. 17, Pakem, Sleman, Yogyakarta" },
  ],
  gallery: ["/themes/img/r16.webp", "/themes/img/r8.webp", "/themes/img/r79.webp", "/themes/img/a111.webp", "/themes/img/r15.webp", "/themes/img/r104.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Nayla Kinanti Sasmita" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0857 2021 0821", account_name: "Raka Adiputra" },
    { id: "demo-kado", type: "address", address: "Jl. Kaliurang Km. 9, Gg. Ngemplak No. 12, Sleman, Yogyakarta 55581" },
  ],
  guestName: "Mbak Sekar & Partner",
});
