import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahmah", groom: "Iqbal",
    brideFull: "Siti Rahmah Ariga, S.Pd.", groomFull: "Muhammad Iqbal Reje Linge, S.P.",
    brideParents: "Putri kedua dari\nBapak Tgk. Abdullah Aman Rahmah & Ibu Hj. Nurlela Inen Rahmah", groomParents: "Putra sulung dari\nBapak Drs. Salman Aman Iqbal & Ibu Fatimah Inen Iqbal",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Seperti kopi Gayo yang dipetik merah dan disangrai dengan sabar, kami ingin rumah tangga yang tumbuh pelan, hangat, dan berkah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-14T09:00:00+07:00",
  place: "Masjid Agung Ruhama Takengon",
  address: "Jl. Masjid Ruhama, Kampung Kemili, Kec. Bebesen, Kabupaten Aceh Tengah",
  stories: [
    { date: "2021", title: "Panen di Bener Meriah", body: "Kami bertemu saat sama-sama menjadi pendamping petani di koperasi kopi. Iqbal mengajari cara memetik ceri yang benar-benar merah." },
    { date: "2024", title: "Secangkir di Tepi Lut Tawar", body: "Obrolan sederhana di kedai kopi tepi danau berubah menjadi niat yang sungguh-sungguh." },
    { date: "Mei 2027", title: "Lamaran Keluarga", body: "Keluarga Iqbal datang meminang secara adat Gayo, disambut kain kerawang dan doa para tetua kampung." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Agung Ruhama Takengon", address: "Jl. Masjid Ruhama, Kampung Kemili, Kec. Bebesen, Kabupaten Aceh Tengah" },
    { name: "Walimatul 'Ursy", date: "2027-08-14T12:00:00+07:00", time: "12.00 – 16.00 WIB", venue: "Kediaman Bapak Tgk. Abdullah", address: "Kampung Bale Atu, Kec. Lut Tawar, Takengon, Kabupaten Aceh Tengah" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a23.webp", "/themes/img/r3.webp", "/themes/img/r4.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7120 4471 09", account_name: "Siti Rahmah Ariga" },
    { id: "demo-aceh", type: "bank", bank_name: "Bank Aceh Syariah", account_number: "0510 2033 1187 2", account_name: "Muhammad Iqbal" },
    { id: "demo-kado", type: "address", address: "Kampung Bale Atu, Kec. Lut Tawar, Takengon, Kabupaten Aceh Tengah 24519", account_name: "Keluarga Tgk. Abdullah" },
  ],
  guestName: "Bapak Reje Kampung Kemili & Keluarga",
  guestTable: "Meja Kerawang 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "12.00", title: "Penyambutan tamu", note: "Didong pembuka dari kelompok kampung" },
      { time: "12.30", title: "Tepung tawar", note: "Doa dan restu para tetua" },
      { time: "13.00", title: "Jamuan makan", note: "Masam jing, kopi Gayo, dan lepat" },
      { time: "15.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim rapi. Hitam, merah, kuning, dan hijau kerawang dipersilakan.", colors: ["#15120e", "#c0322a", "#e7b52c", "#3d8a46"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Tgk. Abdullah Aman Rahmah", "Kel. Besar Drs. Salman Aman Iqbal"] },
  },
});
