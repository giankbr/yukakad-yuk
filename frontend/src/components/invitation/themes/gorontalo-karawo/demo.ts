import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadya", groom: "Rahmat",
    brideFull: "Nadya Fitriani Pakaya, S.Kep.", groomFull: "Rahmat Hidayat Tangahu, S.H.",
    brideParents: "Putri bungsu dari\nBapak H. Hamzah Pakaya & Ibu Hj. Hasna Polapa", groomParents: "Putra kedua dari\nBapak Ismail Tangahu & Ibu Rosmawaty Katili",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti benang karawo yang dihitung satu per satu, kami ingin menyulam hari-hari bersama dengan sabar dan penuh syukur.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T09:00:00+08:00",
  place: "Gedung Karawo Convention, Kota Gorontalo",
  address: "Jl. Nani Wartabone No. 45, Limba U Dua, Kota Selatan, Kota Gorontalo",
  stories: [
    { date: "2019", title: "Pameran Karawo", body: "Rahmat menemani ibunya ke pameran sulaman karawo; Nadya menjaga stan milik kelompok perajin di desanya." },
    { date: "2023", title: "Senja di Limboto", body: "Kami sering bertemu di tepi Danau Limboto selepas Ashar, berbagi binte biluhuta dan cerita tentang masa depan." },
    { date: "2026", title: "Motolobalango", body: "Keluarga Rahmat datang secara adat untuk meminang. Dengan restu kedua keluarga, hari baik pun ditentukan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-21T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Agung Baiturrahim", address: "Jl. Raja Eyato, Biawao, Kota Selatan, Kota Gorontalo" },
    { name: "Resepsi", date: "2027-08-21T19:30:00+08:00", time: "19.30 – 22.00 WITA", venue: "Gedung Karawo Convention", address: "Jl. Nani Wartabone No. 45, Limba U Dua, Kota Gorontalo" },
  ],
  gallery: ["/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/r75.webp", "/themes/img/r13.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Nadya Fitriani Pakaya" },
    { id: "demo-sulutgo", type: "bank", bank_name: "BRI", account_number: "0451 0100 7788 502", account_name: "Rahmat Hidayat Tangahu" },
    { id: "demo-kado", type: "address", address: "Jl. Jaksa Agung Suprapto No. 21, Limba B, Kota Gorontalo 96115" },
  ],
  guestName: "Ibu Hj. Fatma Bouty & Keluarga",
  guestTable: "Meja Saronde 2",
  extras: {
    rundown: { items: [
      { time: "19.30", title: "Kedatangan pengantin", note: "Diiringi tari Saronde" },
      { time: "20.00", title: "Tilawah & doa" },
      { time: "20.15", title: "Ramah tamah", note: "Ilabulo, binte biluhuta, dan kue karawo" },
    ] },
    dressCode: { note: "Busana muslim bernuansa pastel. Lila, mint, dan krem dipersilakan.", colors: ["#b49bd0", "#98cdb9", "#f6eedf", "#e8a3a0"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-21T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Hamzah Pakaya (Limboto)", "Kel. Besar Ismail Tangahu (Kota Gorontalo)"] },
  },
});
