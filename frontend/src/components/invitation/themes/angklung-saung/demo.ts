import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nisa", groom: "Fajar",
    brideFull: "Annisa Rahmawati Sukmana, S.Sn.", groomFull: "Fajar Gumilar Permana, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Dadang Sukmana & Ibu Hj. Iis Rohaeti", groomParents: "Putra sulung dari\nBapak Ujang Supriatna & Ibu Yayah Rukiah",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Dua nada angklung tak pernah berbunyi sendiri; bersama, keduanya menjadi lagu.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T08:00:00+07:00",
  place: "Graha Sanusi Hardjadinata",
  address: "Jl. Dipati Ukur No. 35, Lebakgede, Coblong, Kota Bandung",
  stories: [
    { date: "2019", title: "Satu barisan di latihan angklung", body: "Nisa memegang nada do, Fajar nada sol. Di unit kegiatan angklung kampus, pelatih menempatkan kami berdampingan karena nada kami harus saling menyahut." },
    { date: "2023", title: "Sore di kebun teh Lembang", body: "Setelah lulus, kami tetap bertemu di konser angklung dan menghabiskan sore di kebun teh, bercerita tentang rumah yang ingin kami bangun." },
    { date: "2027", title: "Neundeun omong & lamaran", body: "Keluarga Fajar datang ke Ciumbuleuit membawa niat baik. Dengan restu kedua orang tua, kami melangkah ke pelaminan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-17T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Resepsi & Hiburan Angklung", date: "2027-07-17T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Sanusi Hardjadinata", address: "Jl. Dipati Ukur No. 35, Lebakgede, Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r64.webp", "/themes/img/r57.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bjb", type: "bank", bank_name: "bank bjb", account_number: "0087 2215 6430 100", account_name: "Annisa Rahmawati Sukmana" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7208 1145 39", account_name: "Fajar Gumilar Permana" },
    { id: "demo-kado", type: "address", address: "Jl. Ciumbuleuit No. 118, Hegarmanah, Cidadap, Kota Bandung 40131" },
  ],
  guestName: "Bapak Asep Saepudin & Keluarga",
  guestTable: "Saung 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Mapag panganten", note: "Penyambutan pengantin diiringi angklung dan kendang" },
      { time: "11.30", title: "Sawer & nincak endog", note: "Upacara adat Sunda bersama keluarga" },
      { time: "12.00", title: "Ramah tamah", note: "Nasi timbel, karedok, dan surabi" },
      { time: "13.00", title: "Main angklung bersama tamu" },
    ] },
    dressCode: { note: "Kebaya, batik, atau busana muslim. Nuansa hijau awi, krem bambu, dan cokelat kayu.", colors: ["#3f6b3a", "#e9d39a", "#7a5526", "#f6efdc"] },
    guestPass: {},
    family: { names: ["Kel. Besar H. Dadang Sukmana (Ciumbuleuit)", "Kel. Besar Ujang Supriatna (Lembang)", "Keluarga Paduan Angklung Kampus"] },
  },
});
