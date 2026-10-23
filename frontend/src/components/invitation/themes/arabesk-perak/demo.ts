import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Khalisa", groom: "Fariz",
    brideFull: "Khalisa Najwa Rahmani, S.Ars.", groomFull: "Muhammad Fariz Alamsyah, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ridwan Rahmani & Ibu Hj. Nurul Aini", groomParents: "Putra sulung dari\nBapak Ir. H. Syamsul Alamsyah & Ibu Hj. Rosmawati",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Seperti sulur yang saling menganyam: dua jalan yang tumbuh menjadi satu, tanpa saling memutus.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-11T10:00:00+07:00",
  place: "Balai Sarbini Ballroom",
  address: "Plaza Semanggi, Jl. Jend. Sudirman Kav. 50, Karet Semanggi, Jakarta Selatan",
  stories: [
    { date: "2020", title: "Ruang Studio Lantai Tiga", body: "Satu kelompok tugas di Bandung: Khalisa menggambar ornamen, Fariz menghitung strukturnya. Keduanya sama-sama keras kepala soal detail." },
    { date: "2024", title: "Merantau, lalu Pulang", body: "Tiga tahun bekerja di kota yang berbeda. Jarak justru mengajari kami sabar, dan mendoakan orang yang sama." },
    { date: "2026", title: "Khitbah", body: "Fariz datang bersama keluarganya ke Bogor. Setelah istikharah, kedua keluarga sepakat melangkah bersama." },
    { date: "2027", title: "Akad", body: "Insyaallah kami menyempurnakan separuh agama, memohon doa agar rumah tangga ini tumbuh dalam keberkahan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bintaro Jaya", address: "Jl. Bintaro Utama 3A, Pondok Karya, Pondok Aren, Tangerang Selatan" },
    { name: "Walimah", date: "2027-09-11T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Sarbini Ballroom", address: "Plaza Semanggi, Jl. Jend. Sudirman Kav. 50, Karet Semanggi, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a83.webp", "/themes/img/a118.webp", "/themes/img/a84.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7215 0093 46", account_name: "Khalisa Najwa Rahmani" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1240 0118 7763", account_name: "Muhammad Fariz Alamsyah" },
    { id: "demo-kado", type: "address", address: "Jl. Pajajaran Indah V No. 14, Baranangsiang, Bogor Timur, Kota Bogor 16143" },
  ],
  guestName: "Bapak H. Anwar Zulkarnain & Keluarga",
  guestTable: "Meja Perak 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan mempelai", note: "Diiringi marawis" },
      { time: "11.20", title: "Tausiyah walimah", note: "Ustadz H. Abdul Hakim, Lc." },
      { time: "11.50", title: "Doa bersama & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim formal. Hitam, abu perak, dan putih gading dipersilakan.", colors: ["#0c0b0e", "#a4afc6", "#e9e6df", "#4b4f5a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ridwan Rahmani", "Kel. Besar Ir. H. Syamsul Alamsyah"] },
  },
});
