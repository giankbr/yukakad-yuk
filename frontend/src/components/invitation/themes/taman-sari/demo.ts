import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Larasati", groom: "Bagas",
    brideFull: "Larasati Wening Pangastuti, S.Ars.", groomFull: "Bagas Adi Prakoso, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Sumarno Hadi & Ibu Hj. Retno Wulandari", groomParents: "Putra sulung dari\nBapak Drs. Joko Prakoso & Ibu Endang Sulistyowati",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti air kolam Taman Sari yang jernih dan tenang, semoga rumah tangga kami selalu menyejukkan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T09:00:00+07:00",
  place: "Pendopo Agung Royal Ambarrukmo",
  address: "Jl. Laksda Adisucipto No. 81, Ambarukmo, Caturtunggal, Depok, Sleman, Yogyakarta",
  stories: [
    { date: "2020", title: "Sketsa di Gapura", body: "Larasati sedang menggambar gapura Taman Sari untuk tugas kuliah arsitektur ketika Bagas menawarkan payung karena gerimis turun." },
    { date: "2023", title: "Jalan Pulang yang Sama", body: "Tiga tahun menyusuri lorong Sumur Gumuling dan kampung Patehan, kami belajar saling menunggu dan saling menguatkan." },
    { date: "2027", title: "Menuju Kolam yang Tenang", body: "Dengan restu kedua orang tua, kami melangkah ke jenjang pernikahan di kota yang mempertemukan kami." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Gedhe Kauman", address: "Jl. Kauman, Ngupasan, Gondomanan, Yogyakarta" },
    { name: "Resepsi", date: "2027-08-14T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Pendopo Agung Royal Ambarrukmo", address: "Jl. Laksda Adisucipto No. 81, Ambarukmo, Caturtunggal, Depok, Sleman, Yogyakarta" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a49.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a50.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4560 88", account_name: "Larasati Wening Pangastuti" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "137 00 1928374 5", account_name: "Bagas Adi Prakoso" },
    { id: "demo-kado", type: "address", address: "Jl. Taman, Patehan, Kraton, Yogyakarta 55133" },
  ],
  guestName: "Ibu Dra. Sri Handayani & Keluarga",
  guestTable: "Umbul Binangun 2",
  extras: {
    rundown: { items: [
      { time: "18.30", title: "Kirab pengantin", note: "Diiringi gendhing Ladrang Wilujeng" },
      { time: "19.00", title: "Sambutan keluarga & doa" },
      { time: "19.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana batik atau kebaya. Nuansa krem, toska, dan coklat muda dipersilakan.", colors: ["#efe4cb", "#5fbfb8", "#b8925a", "#23787a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak H. Sumarno Hadi", "Kel. Besar Bapak Drs. Joko Prakoso"] },
  },
});
