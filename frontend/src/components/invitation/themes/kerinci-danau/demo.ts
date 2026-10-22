import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nurul", groom: "Fadhil",
    brideFull: "Nurul Azizah Depati, S.Farm.", groomFull: "Fadhil Rahman, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Zulkarnain Depati & Ibu Hj. Rosmaini", groomParents: "Putra kedua dari\nBapak Syamsul Bahri & Ibu Yusnidar",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Di kaki Gunung Kerinci kami belajar bahwa yang tinggi tetap butuh pijakan, dan yang tenang seperti danau justru paling dalam.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-26T09:00:00+07:00",
  place: "Masjid Agung Pondok Tinggi",
  address: "Jl. Depati Parbo, Pondok Tinggi, Kec. Sungai Penuh, Kota Sungai Penuh, Jambi",
  stories: [
    { date: "2020", title: "Pendakian Pertama", body: "Rombongan pendaki kampus berangkat dari Kersik Tuo. Fadhil membawakan carrier Nurul yang terlalu berat sampai Shelter 2." },
    { date: "2023", title: "Pulang ke Sungai Penuh", body: "Nurul membuka apotek di kampung, Fadhil bertugas di proyek irigasi Kerinci. Kami bertemu lagi di acara kenduri sko." },
    { date: "April 2027", title: "Ikat Janji", body: "Keluarga datang ke rumah larik nenek, ninik mamak bermufakat, dan tanggal baik pun ditetapkan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-26T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Agung Pondok Tinggi", address: "Jl. Depati Parbo, Pondok Tinggi, Kec. Sungai Penuh, Kota Sungai Penuh, Jambi" },
    { name: "Walimatul 'Ursy", date: "2027-06-26T11:30:00+07:00", time: "11.30 – 16.00 WIB", venue: "Rumah Larik Keluarga Depati", address: "Dusun Sungai Penuh, Kec. Pesisir Bukit, Kota Sungai Penuh, Jambi" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r104.webp", "/themes/img/a99.webp", "/themes/img/r29.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7213 5580 22", account_name: "Nurul Azizah" },
    { id: "demo-jambi", type: "bank", bank_name: "Bank Jambi", account_number: "1302 0045 7781", account_name: "Fadhil Rahman" },
    { id: "demo-kado", type: "address", address: "Dusun Sungai Penuh, Kec. Pesisir Bukit, Kota Sungai Penuh, Jambi 37112", account_name: "Keluarga H. Zulkarnain Depati" },
  ],
  guestName: "Bapak Depati Rajo Mudo & Keluarga",
  guestTable: "Meja Kayu Aro 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.30", title: "Penyambutan tamu", note: "Iringan rebana dan tari iyo-iyo" },
      { time: "12.00", title: "Pepatah-petitih adat", note: "Disampaikan ninik mamak kedua keluarga" },
      { time: "12.30", title: "Makan bersama", note: "Gulai ikan semah dan teh Kayu Aro" },
      { time: "15.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim rapi bernuansa alam Kerinci: hijau teh, biru danau, cokelat kayu.", colors: ["#5f9440", "#6f87a4", "#4a2a19", "#d9a441"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkarnain Depati", "Kel. Besar Syamsul Bahri"] },
  },
});
