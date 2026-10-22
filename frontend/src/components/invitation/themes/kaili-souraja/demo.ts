import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Dila", groom: "Fikri",
    brideFull: "Sitti Nurfadilah Lamadjido, S.Pd.", groomFull: "Moh. Fikri Pettalolo, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Rusdy Lamadjido & Ibu Hj. Nurhayati Lasaka", groomParents: "Putra sulung dari\nBapak Drs. Amiruddin Pettalolo & Ibu Rosmiati Labaso",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Seperti benang sarung Donggala yang ditenun helai demi helai, kami ingin merajut hari-hari bersama dengan sabar, rapi, dan penuh syukur.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T09:00:00+08:00",
  place: "Gedung Serbaguna Lere, Palu Barat",
  address: "Jl. Raja Moili No. 12, Lere, Palu Barat, Kota Palu, Sulawesi Tengah",
  stories: [
    { date: "2020", title: "Senja di Talise", body: "Kami berkenalan di sebuah kegiatan relawan di Pantai Talise. Selepas bekerja, kami duduk memandang teluk sampai azan Magrib." },
    { date: "2023", title: "Menenun Rencana", body: "Dila mengajar di Donggala, Fikri bekerja di Palu. Setiap akhir pekan kami bertemu di tengah jalan, berbagi kaledo dan cerita." },
    { date: "2026", title: "Lamaran", body: "Keluarga Fikri datang meminang dengan adat dan doa. Kedua keluarga sepakat, hari baik pun ditetapkan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Nurul Huda Lere", address: "Jl. Cumi-Cumi No. 3, Lere, Palu Barat, Kota Palu" },
    { name: "Resepsi", date: "2027-09-18T19:00:00+08:00", time: "19.00 – 22.00 WITA", venue: "Gedung Serbaguna Lere", address: "Jl. Raja Moili No. 12, Lere, Palu Barat, Kota Palu" },
  ],
  gallery: ["/themes/img/r2.webp", "/themes/img/r104.webp", "/themes/img/a95.webp", "/themes/img/r3.webp", "/themes/img/r29.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7204 1188 35", account_name: "Sitti Nurfadilah Lamadjido" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0187 0100 4521 509", account_name: "Moh. Fikri Pettalolo" },
    { id: "demo-kado", type: "address", address: "Jl. Towua No. 27, Tatura Selatan, Palu Selatan, Kota Palu 94236" },
  ],
  guestName: "Bapak Ir. Hasanuddin Tombolotutu & Keluarga",
  guestTable: "Meja Donggala 3",
  extras: {
    rundown: { items: [
      { time: "19.00", title: "Kedatangan pengantin", note: "Diiringi rebana dan tarian penyambutan" },
      { time: "19.30", title: "Tilawah & doa" },
      { time: "20.00", title: "Ramah tamah", note: "Kaledo, uta dada, dan kue tradisional Kaili" },
    ] },
    dressCode: { note: "Busana muslim atau batik. Nuansa ungu, magenta, dan emas ala sarung Donggala dipersilakan.", colors: ["#4a1838", "#b23a6e", "#c79a3e", "#2f6b55"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Rusdy Lamadjido (Donggala)", "Kel. Besar Drs. Amiruddin Pettalolo (Palu)"] },
  },
});
