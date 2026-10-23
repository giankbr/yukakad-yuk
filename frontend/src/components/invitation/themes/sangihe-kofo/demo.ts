import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Febiola", groom: "Rivaldo",
    brideFull: "Febiola Grace Kansil, S.Pd.", groomFull: "Rivaldo Yohanes Makagansa, S.Kom.",
    brideParents: "Putri sulung dari\nBapak Yance Kansil & Ibu Netty Lahope", groomParents: "Putra kedua dari\nBapak Jemmy Makagansa & Ibu Selvi Tatoda",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti benang abaka yang dipintal satu per satu lalu ditenun menjadi kofo, kami ingin saling menguatkan dan menjadi satu kain yang utuh.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T10:00:00+08:00",
  place: "Gedung Serbaguna Tahuna",
  address: "Jl. Makaampo No. 21, Tahuna, Kabupaten Kepulauan Sangihe, Sulawesi Utara",
  stories: [
    { date: "2019", title: "Pesta Tulude", body: "Kami pertama kali bertemu saat persiapan Tulude di jemaat. Febiola memimpin paduan suara, Rivaldo sibuk menata panggung dari bambu." },
    { date: "2023", title: "Kapal ke Manado", body: "Berbulan-bulan kami berpisah karena kuliah. Setiap kapal dari Pelabuhan Tahuna membawa surat dan rindu, lalu pulang membawa jawaban." },
    { date: "2026", title: "Masuk minta", body: "Keluarga Makagansa datang dengan perahu dari Manganitu. Di bawah Gunung Awu yang tenang, dua keluarga sepakat menyatukan kami." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-06-19T10:00:00+08:00", time: "10.00 – 11.30 WITA", venue: "Gereja GMIST Jemaat Imanuel Tahuna", address: "Jl. Raramenusa No. 5, Tahuna, Kabupaten Kepulauan Sangihe" },
    { name: "Resepsi", date: "2027-06-19T18:00:00+08:00", time: "18.00 – 21.00 WITA", venue: "Gedung Serbaguna Tahuna", address: "Jl. Makaampo No. 21, Tahuna, Kabupaten Kepulauan Sangihe" },
  ],
  gallery: ["/themes/img/r109.webp", "/themes/img/r38.webp", "/themes/img/r107.webp", "/themes/img/r110.webp", "/themes/img/r106.webp", "/themes/img/r105.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0123 0100 8812 503", account_name: "Febiola Grace Kansil" },
    { id: "demo-bsg", type: "bank", bank_name: "SulutGo", account_number: "003 02 11 07788 1", account_name: "Rivaldo Yohanes Makagansa" },
    { id: "demo-kado", type: "address", address: "Jl. Towoliu No. 9, Kelurahan Santiago, Tahuna 95812" },
  ],
  guestName: "Bapak Hendro Pandensolang & Keluarga",
  guestTable: "Meja Awu 3",
  extras: {
    rundown: { items: [
      { time: "18.00", title: "Penyambutan pengantin", note: "Diiringi musik bambu dan tari Gunde" },
      { time: "18.30", title: "Doa syukur & sambutan keluarga" },
      { time: "19.00", title: "Makan bersama", note: "Ikan bakar, tinutuan, dan kue bagea sagu" },
      { time: "20.00", title: "Masamper & foto bersama" },
    ] },
    dressCode: { note: "Kain kofo, tenun, atau batik. Nuansa natural, biru laut, dan karat dipersilakan.", colors: ["#cdb383", "#9f4426", "#283f66", "#efe3c4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-19T10:00:00+08:00" },
    rsvpDietary: {},
    family: { names: ["Kel. Besar Kansil – Lahope (Tahuna)", "Kel. Besar Makagansa – Tatoda (Manganitu)"] },
  },
});
