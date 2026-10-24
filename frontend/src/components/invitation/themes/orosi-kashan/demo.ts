import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Fikri",
    brideFull: "Zahra Khairunnisa, S.Ars.", groomFull: "Muhammad Fikri Ramadhan, S.T.",
    brideParents: "Putri bungsu dari\nBapak Ir. H. Ahmad Syarifuddin & Ibu Hj. Nurlaila", groomParents: "Putra kedua dari\nBapak H. Abdul Rahman & Ibu Hj. Siti Maryam",
    note: "Seperti cahaya yang melewati kaca berwarna, semoga cinta kami menjadi lebih indah karena saling melengkapi.",
  },
  eventLabel: "Walimatul 'Urs",
  date: "2027-06-12T08:00:00+07:00",
  place: "Hotel Savoy Homann",
  address: "Jl. Asia Afrika No. 112, Paledang, Lengkong, Bandung",
  stories: [
    { date: "2019", title: "Studio Arsitektur", body: "Kami satu kelompok tugas studio di Bandung. Zahra menggambar denah, Fikri menghitung struktur, dan kami sering berdebat soal letak jendela." },
    { date: "2023", title: "Rumah-Rumah Tua", body: "Zahra meneliti rumah-rumah berhalaman tengah untuk tesisnya. Fikri menemani memotret setiap jendela kaca warna yang mereka temui." },
    { date: "2026", title: "Khitbah", body: "Selepas shalat Isya, keluarga Fikri datang melamar dengan sederhana. Bismillah, kami memilih untuk melangkah bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung" },
    { name: "Walimah", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Hotel Savoy Homann", address: "Jl. Asia Afrika No. 112, Paledang, Lengkong, Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7134 5520 18", account_name: "Zahra Khairunnisa" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Barat No. 21, Cibeunying Kaler, Bandung 40191" },
  ],
  guestName: "Ibu Hj. Ratna Dewi & Keluarga",
  guestTable: "Meja Firuzeh 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu" },
      { time: "11.30", title: "Doa & tausiyah singkat", note: "Ustadz H. Hilman Fauzi" },
      { time: "12.00", title: "Ramah tamah & santap siang" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim. Nuansa pirus, merah delima, dan kuning kunyit dipersilakan.", colors: ["#2a4fa8", "#b8233a", "#e8a52a", "#2c8a5c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar H. Abdul Rahman"] },
  },
});
