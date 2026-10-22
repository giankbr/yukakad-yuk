import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nisa", groom: "Fikri",
    brideFull: "Annisa Rahmawati Sukmana, S.P.", groomFull: "Muhammad Fikri Ramdhani, S.TP.",
    brideParents: "Putri bungsu dari\nBapak H. Asep Sukmana & Ibu Hj. Euis Kurniasih",
    groomParents: "Putra kedua dari\nBapak Dadang Ramdhani & Ibu Neneng Hasanah",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a126.webp",
    note: "Tumbuh pelan seperti pucuk teh di lereng Puncak: dirawat setiap pagi, dipetik pada waktunya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T08:00:00+07:00",
  place: "Pendopo Kebun Teh Gunung Mas",
  address: "Jl. Raya Puncak Km. 87, Tugu Selatan, Cisarua, Kabupaten Bogor",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2017", title: "Praktik lapang", body: "Kami satu kelompok praktik lapang di perkebunan teh. Fikri mencatat suhu, Nisa menghitung pucuk, dan kami sama-sama kehujanan di pondok kayu." },
    { date: "2022", title: "Pulang ke Bogor", body: "Setelah bekerja di kota berbeda, kami kembali ke Bogor dan mulai rutin bersepeda ke Puncak setiap Ahad pagi." },
    { date: "2026", title: "Silaturahmi keluarga", body: "Keluarga Fikri datang meminang di rumah Nisa di Cipanas, ditemani teh hangat dan kabut sore." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-17T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jami' Al-Ikhlas Tugu Selatan", address: "Jl. Raya Puncak Gg. Masjid No. 3, Tugu Selatan, Cisarua, Kabupaten Bogor" },
    { name: "Resepsi di Kebun", date: "2027-07-17T10:30:00+07:00", time: "10.30 – 14.00 WIB", venue: "Pendopo Kebun Teh Gunung Mas", address: "Jl. Raya Puncak Km. 87, Tugu Selatan, Cisarua, Kabupaten Bogor" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/a116.webp", "/themes/img/a26.webp", "/themes/img/a95.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BJB", account_number: "0087 2210 5543", account_name: "Annisa Rahmawati Sukmana" },
    { id: "demo-kado", type: "address", address: "Jl. Pasir Kampung No. 21, Cipanas, Kabupaten Cianjur 43253" },
  ],
  guestName: "Bapak Ujang Suryana & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.30", title: "Resepsi di pendopo", note: "Degung Sunda & sajian teh Puncak" },
      { time: "12.00", title: "Ramah tamah & foto bersama", note: "Di antara barisan kebun teh" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Nuansa hijau pupus dan krem. Bawa jaket tipis, udara Puncak sejuk.", colors: ["#6fa548", "#c4dc7a", "#f2ead6", "#a8774c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Keluarga Besar H. Asep Sukmana", "Keluarga Besar Dadang Ramdhani", "Rekan Agronomi IPB Angkatan 51"] },
    travel: { note: "Jalur Puncak padat di akhir pekan. Kami sarankan berangkat sebelum pukul 06.30 atau lewat jalur alternatif.", items: [
      { name: "Parkir pengunjung Gunung Mas", detail: "Area parkir utama, shuttle ke pendopo tiap 10 menit" },
      { name: "Penginapan di Tugu Selatan", detail: "Beberapa vila keluarga tersedia, hubungi panitia" },
    ] },
    faq: { items: [
      { q: "Apakah lokasi ramah lansia?", a: "Pendopo bisa dicapai dengan mobil sampai depan. Area foto di kebun bersifat opsional." },
      { q: "Bagaimana jika hujan?", a: "Pendopo beratap penuh, acara tetap berlangsung meski gerimis." },
    ] },
  },
});
