import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Bagas",
    note: "Sederhana saja: rumah kecil, secangkir kopi, dan kamu.",
    brideFull: "Sekar Ayuningtyas, S.P.", groomFull: "Bagas Adi Nugraha",
    brideParents: "Putri bungsu dari\nBapak Suparno & Ibu Sri Wahyuni",
    groomParents: "Putra kedua dari\nBapak Darmanto & Ibu Tutik Handayani",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r4.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T08:00:00+07:00",
  place: "Omah Kebon Kaliurang",
  address: "Jl. Kaliurang Km. 17, Pakem, Sleman, Yogyakarta",
  stories: [
    { date: "2017", title: "Kebun Bunga Matahari", body: "Bertemu saat KKN di lereng Merapi. Sekar mengajar anak-anak menanam bunga matahari, Bagas sibuk membetulkan pagar bambu." },
    { date: "2021", title: "Kedai Kopi Pertama", body: "Bersama membuka kedai kopi kecil di Pakem. Meja dan kursinya dibuat sendiri dari kayu bekas." },
    { date: "2026", title: "Sebuah Pertanyaan", body: "Di bawah pohon trembesi depan kedai, Bagas bertanya sambil gemetar. Sekar menjawab dengan anggukan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Ikhlas Pakem", address: "Jl. Kaliurang Km. 17,5, Pakembinangun, Sleman" },
    { name: "Syukuran Kebun", date: "2027-07-10T10:30:00+07:00", time: "10.30 – 14.00 WIB", venue: "Omah Kebon Kaliurang", address: "Jl. Kaliurang Km. 17, Pakem, Sleman, Yogyakarta" },
  ],
  gallery: ["/themes/img/r8.webp", "/themes/img/a111.webp", "/themes/img/r79.webp", "/themes/img/r16.webp", "/themes/img/r44.webp", "/themes/img/r65.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0029 0102 3344 507", account_name: "Sekar Ayuningtyas" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0857 2910 4455", account_name: "Bagas Adi Nugraha" },
    { id: "demo-kado", type: "address", address: "Jl. Kaliurang Km. 17, Pakem, Sleman, Yogyakarta 55582" },
  ],
  guestName: "Mas Yoga & Keluarga",
});
