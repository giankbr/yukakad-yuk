import { makeDemo } from "../demo-base";

// Pernikahan adat Tidung di Kota Tarakan, Kalimantan Utara: akad di masjid, lalu bersanding di balai adat Baloy.
export const demo = makeDemo({
  couple: {
    bride: "Hasnah", groom: "Ridwan",
    brideFull: "Dayang Siti Hasnah, S.Pd.", groomFull: "Awang Muhammad Ridwan, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Abdul Kadir & Ibu Hj. Dayang Rosnah", groomParents: "Putra sulung dari\nBapak Datu Hamzah Idris & Ibu Nurlela",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti tiang ulin Baloy yang berdiri kokoh di atas laut, semoga rumah tangga kami teguh diterpa pasang dan surut.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T09:00:00+08:00",
  place: "Balai Adat Baloy Mayo",
  address: "Kompleks Baloy Mayo Adat Tidung, Tarakan Barat, Kota Tarakan, Kalimantan Utara",
  stories: [
    { date: "2020", title: "Senja di Pantai Amal", body: "Bertemu saat sama-sama menjadi panitia festival budaya Iraw Tengkayu di Tarakan." },
    { date: "2024", title: "Belajar Adat", body: "Hasnah mengajari Ridwan tari Jepen, Ridwan belajar berpantun untuk keluarga besar Hasnah." },
    { date: "2027", title: "Bersanding di Baloy", body: "Dengan restu kedua keluarga besar, kami melangkah menuju ikatan suci pernikahan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+08:00", time: "08.00 – 09.30 WITA", venue: "Masjid Agung Baitul Izzah", address: "Jl. Jenderal Sudirman, Pamusian, Tarakan Tengah, Kota Tarakan" },
    { name: "Bersanding & Resepsi", date: "2027-08-14T11:00:00+08:00", time: "11.00 – 15.00 WITA", venue: "Balai Adat Baloy Mayo", address: "Kompleks Baloy Mayo Adat Tidung, Tarakan Barat, Kota Tarakan, Kalimantan Utara" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/r57.webp", "/themes/img/r58.webp", "/themes/img/a99.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bankaltimtara", account_number: "0031 2087 6542", account_name: "Dayang Siti Hasnah" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "DANA", ewallet_number: "0812 5530 1427", account_name: "Awang Muhammad Ridwan" },
    { id: "demo-kado", type: "address", address: "Jl. Yos Sudarso No. 27, Selumit Pantai, Tarakan Tengah, Kota Tarakan 77113" },
  ],
  guestName: "Bapak H. Burhanuddin & Keluarga",
  guestTable: "Serambi 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan rombongan pengantin", note: "Diiringi hadrah & tari Jepen" },
      { time: "11.30", title: "Bersanding di pelaminan Baloy" },
      { time: "12.15", title: "Doa & ramah tamah", note: "Hidangan khas pesisir Tidung" },
    ] },
    dressCode: { note: "Busana muslim atau baju adat. Hijau, kuning, dan merah dipersilakan.", colors: ["#1f6b4a", "#f0c234", "#c4372c", "#123f3d"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Kadir", "Kel. Besar Datu Hamzah Idris", "Lembaga Adat Tidung Kota Tarakan"] },
    travel: { note: "Untuk tamu dari luar Tarakan, berikut pilihan terdekat.", items: [
      { name: "Bandara Juwata Tarakan", detail: "± 15 menit berkendara ke Baloy Mayo" },
      { name: "Pelabuhan Tengkayu", detail: "Speedboat dari Tanjung Selor & Nunukan" },
    ] },
  },
});
