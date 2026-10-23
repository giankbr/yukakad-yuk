import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Muhammad Ridwan", groom: "Siti Rahmah",
    brideFull: "Bapak H. Muhammad Ridwan", groomFull: "Ibu Hj. Siti Rahmah",
    brideParents: "Jamaah haji Kloter BDJ-07\nEmbarkasi Banjarmasin", groomParents: "Mendampingi dalam satu rombongan\nKBIH Al-Mabrur Banjarmasin",
    note: "Alhamdulillah, Allah memudahkan setiap langkah dan memulangkan kami dalam keadaan sehat. Mohon doakan agar haji kami mabrur dan membawa kebaikan bagi keluarga dan kampung kami.",
  },
  eventLabel: "Tasyakuran Kepulangan Haji",
  date: "2027-06-26T09:00:00+08:00",
  place: "Kediaman Keluarga H. Muhammad Ridwan",
  address: "Jl. Pramuka Komp. Semanda Indah No. 27, Pemurus Luar, Banjarmasin Timur, Kota Banjarmasin",
  stories: [
    { date: "2013", title: "Niat & Menabung", body: "Dari hasil berdagang kain sasirangan di Pasar Sudimampir, kami menabung sedikit demi sedikit dan mendaftar porsi haji." },
    { date: "2026", title: "Panggilan Pelunasan", body: "Setelah tiga belas tahun menanti, nama kami masuk daftar pelunasan. Manasik diikuti setiap pekan bersama rombongan." },
    { date: "Mei 2027", title: "Berangkat ke Tanah Suci", body: "Dilepas keluarga dan tetangga dari Asrama Haji Landasan Ulin, berangkat bersama Kloter BDJ-07." },
    { date: "Juni 2027", title: "Kembali ke Rumah", body: "Alhamdulillah, seluruh rangkaian ibadah tertunaikan dan kami kembali dengan selamat. Saatnya bersyukur bersama." },
  ],
  events: [
    { name: "Penyambutan Kepulangan", date: "2027-06-24T14:00:00+08:00", time: "14.00 WITA (menyesuaikan jadwal kloter)", venue: "Asrama Haji Embarkasi Banjarmasin", address: "Jl. A. Yani Km. 23, Landasan Ulin, Banjarbaru" },
    { name: "Tasyakuran & Doa Bersama", date: "2027-06-26T09:00:00+08:00", time: "09.00 – 12.00 WITA", venue: "Kediaman Keluarga H. Muhammad Ridwan", address: "Jl. Pramuka Komp. Semanda Indah No. 27, Pemurus Luar, Banjarmasin Timur" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-santunan", type: "bank", bank_name: "BSI", account_number: "7177 2027 01", account_name: "Santunan Yatim Musala Al-Ikhlas" },
  ],
  guestName: "Bapak H. Fahrurrazi & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan sempurnakanlah ibadah haji dan umrah karena Allah.", source: "QS. Al-Baqarah: 196" },
    rundown: { items: [
      { time: "09.00", title: "Pembukaan & tilawah" },
      { time: "09.30", title: "Kisah perjalanan & tausiyah", note: "Ustaz H. Ahmad Zaini" },
      { time: "10.30", title: "Doa bersama & pembacaan maulid" },
      { time: "11.00", title: "Ramah tamah, air zamzam & kurma" },
    ] },
    dressCode: { note: "Busana muslim rapi. Putih dan hijau lembut dipersilakan.", colors: ["#ffffff", "#cfe0d2", "#8fb29a", "#c8a45a"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar H. Muhammad Ridwan", "Jamaah Musala Al-Ikhlas Semanda"] },
    faq: { items: [
      { q: "Apakah ada oleh-oleh?", a: "Insyaallah tersedia air zamzam dan kurma untuk setiap keluarga yang hadir." },
      { q: "Di mana parkir kendaraan?", a: "Parkir tersedia di halaman Musala Al-Ikhlas, sekitar 40 meter dari rumah." },
    ] },
  },
});
