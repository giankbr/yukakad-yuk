import { makeDemo } from "../demo-base";

// Adat Sunda, Garut: akad nikah di masjid agung alun-alun, lalu resepsi di aula tepi Situ Bagendit dengan latar Gunung Cikuray.
export const demo = makeDemo({
  couple: {
    bride: "Ratna", groom: "Yusuf",
    brideFull: "Ratna Kurniasih, S.Pd.", groomFull: "Yusuf Maulana Saputra, S.T.",
    brideParents: "Putri kadua ti\nBapak H. Dedi Rusmana & Ibu Hj. Euis Komariah", groomParents: "Putra cikal ti\nBapak Aceng Hidayat & Ibu Nenden Sumiati",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Sapertos lereng dina samping batik: ngarambat lalaunan, sajajar, tur teu pegat.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T08:00:00+07:00",
  place: "Aula Saung Bagendit",
  address: "Jl. Raya Bagendit No. 21, Bagendit, Kec. Banyuresmi, Kabupaten Garut",
  stories: [
    { date: "2020", title: "Tepang di Rumah Batik", body: "Ratna sedang belajar mencanting di sebuah rumah batik di Garut Kota, Yusuf datang mengantar pesanan kain untuk ibunya." },
    { date: "2024", title: "Neundeun Omong", body: "Keluarga Yusuf bersilaturahmi ke rumah Ratna di Tarogong, menitipkan niat baik untuk melamar." },
    { date: "2027", title: "Ijab Kabul", body: "Insyaallah kami mengikat janji suci di kaki Gunung Cikuray, dengan restu sepuh dan keluarga besar." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Garut", address: "Jl. Alun-Alun Barat, Kel. Paminggir, Kec. Garut Kota, Kabupaten Garut" },
    { name: "Resepsi", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Saung Bagendit", address: "Jl. Raya Bagendit No. 21, Bagendit, Kec. Banyuresmi, Kabupaten Garut" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/a22.webp", "/themes/img/r1.webp", "/themes/img/r57.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BJB", account_number: "0071 2027 0619 3", account_name: "Ratna Kurniasih" },
    { id: "demo-kado", type: "address", address: "Jl. Pembangunan No. 88, Tarogong Kidul, Kabupaten Garut 44151" },
  ],
  guestName: "Bapak H. Ujang Sutisna & Kulawarga",
  guestTable: "Meja Lereng 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Mapag panganten", note: "Diiringi kacapi suling" },
      { time: "11.30", title: "Saweran & huap lingkung" },
      { time: "12.00", title: "Ramah tamah: nasi liwet, dodol, dan burayot Garut" },
      { time: "13.30", title: "Poto babarengan" },
    ] },
    dressCode: { note: "Busana sopan bernuansa batik Garutan: krem gumading, cokelat soga, biru, dan hijau lembut.", colors: ["#efe2c3", "#94603a", "#41627d", "#7d9168"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dedi Rusmana (Tarogong)", "Kel. Besar Aceng Hidayat (Bayongbong)"] },
    travel: { note: "Lokasi resepsi di tepi Situ Bagendit, sekitar 20 menit dari pusat kota.", items: [
      { name: "Dari Alun-Alun Garut", detail: "± 20 menit via Jl. Raya Bagendit" },
      { name: "Parkir", detail: "Halaman aula dan lapangan desa, dipandu panitia" },
    ] },
  },
});
