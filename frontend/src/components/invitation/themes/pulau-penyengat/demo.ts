import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Atikah", groom: "Faiz",
    brideFull: "Raja Nur Atikah", groomFull: "Muhammad Faiz Al-Hadi",
    brideParents: "Putri dari Bapak Raja Hamzah Yunus\n& Ibu Hj. Wan Rosnah", groomParents: "Putra dari Bapak H. Syahrial Hadi\n& Ibu Tengku Zuraida",
    bridePhoto: "/themes/img/a62.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Pompong berlayar ke Pulau Penyengat,\nMasjid kuning berdiri megah;\nKami bersanding dalam ikatan yang kuat,\nMohon doa restu agar penuh berkah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T08:30:00+07:00",
  place: "Masjid Raya Sultan Riau Pulau Penyengat",
  address: "Kelurahan Penyengat, Kec. Tanjungpinang Kota, Kota Tanjungpinang, Kepulauan Riau",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Satu Pompong", body: "Kami sering duduk di pompong yang sama dari Pelantar Kuning menuju Penyengat, Atikah ke rumah nenek, Faiz ke sanggar gurindam." },
    { date: "2024", title: "Gurindam Dua Belas", body: "Berjumpa lagi di Festival Pulau Penyengat. Faiz membaca gurindam, Atikah menyiapkan kue bangkit di tenda sebelah." },
    { date: "Feb 2027", title: "Merisik & Meminang", body: "Keluarga Faiz datang merisik, lalu meminang dengan tepak sirih dan tanda pinangan. Kedua keluarga bermufakat." },
    { date: "Agustus 2027", title: "Bersanding", body: "Insyaallah akad di masjid yang sejak kecil kami pandang dari seberang, lalu bersanding di Tanjungpinang." },
  ],
  events: [
    { name: "Malam Berinai", date: "2027-08-20T19:30:00+07:00", time: "19.30 WIB – selesai", venue: "Kediaman Keluarga Raja Hamzah", address: "Jl. Raja Haji Fisabilillah, Kelurahan Penyengat, Tanjungpinang" },
    { name: "Akad Nikah", date: "2027-08-21T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Raya Sultan Riau Pulau Penyengat", address: "Kelurahan Penyengat, Kec. Tanjungpinang Kota, Kepulauan Riau" },
    { name: "Kenduri & Bersanding", date: "2027-08-21T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung Daerah Tanjungpinang", address: "Jl. Pos No. 1, Tanjungpinang Kota, Kota Tanjungpinang" },
  ],
  gallery: ["/themes/img/a61.webp", "/themes/img/a62.webp", "/themes/img/a63.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7212 0821 27", account_name: "Raja Nur Atikah" },
    { id: "demo-riau", type: "bank", bank_name: "Riau Kepri Syariah", account_number: "8100 2027 0821", account_name: "Muhammad Faiz Al-Hadi" },
  ],
  guestName: "Bapak Datuk H. Abdul Malik & Keluarga",
  guestTable: "Hamparan 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin & silat pengiring" },
      { time: "11.30", title: "Tepuk tepung tawar", note: "Oleh keluarga dan tetua adat" },
      { time: "12.00", title: "Bersanding di pelaminan" },
      { time: "12.30", title: "Makan beradab bersama" },
    ] },
    dressCode: { note: "Baju kurung atau teluk belanga. Kuning, hijau, dan krem dipersilakan.", colors: ["#e6b92e", "#23603f", "#fbf4e0", "#3c8f87"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Raja Hamzah Yunus", "Keluarga Besar H. Syahrial Hadi", "Lembaga Adat Melayu Kelurahan Penyengat"] },
    travel: { note: "Menuju Pulau Penyengat dari Tanjungpinang.", items: [
      { name: "Pompong dari Pelantar Kuning", detail: "± 15 menit, berangkat setiap kapal penuh. Rombongan keluarga pukul 07.45" },
      { name: "Bandara Raja Haji Fisabilillah", detail: "± 25 menit berkendara ke Pelantar Kuning" },
    ] },
    faq: { items: [
      { q: "Apakah perlu membawa pakaian khusus ke masjid?", a: "Mohon berbusana muslim yang menutup aurat. Kain sarung dan selendang tersedia di serambi." },
      { q: "Bagaimana kembali ke Tanjungpinang?", a: "Pompong kembali hingga sore hari. Panitia menyiapkan pompong khusus tamu pukul 10.15." },
    ] },
  },
});
