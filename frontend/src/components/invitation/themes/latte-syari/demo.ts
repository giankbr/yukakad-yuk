import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hana", groom: "Yusuf",
    brideFull: "Hana Salsabila Putri, S.Ars.", groomFull: "Yusuf Abdurrahman Hakim, S.E.",
    brideParents: "Putri pertama dari\nBapak H. Ahmad Syarifuddin & Ibu Hj. Siti Maemunah",
    groomParents: "Putra ketiga dari\nBapak Abdul Hakim & Ibu Nur Hidayati",
    note: "Seperti kopi dan susu yang menyatu tanpa saling menghapus, semoga kami saling melengkapi dalam ridha-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-21T08:00:00+07:00",
  place: "Masjid Al-Ikhlas Dinoyo",
  address: "Jl. MT Haryono No. 12, Dinoyo, Kec. Lowokwaru, Kota Malang",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2024", title: "Kajian Ahad Pagi", body: "Kami sama-sama menjadi relawan konsumsi di kajian pekanan masjid kampus. Yusuf yang menyeduh kopi, Hana yang menata hidangan." },
    { date: "2026", title: "Ta'aruf", body: "Melalui ustadzah pembimbing, kami bertukar biodata dan bertemu dengan didampingi keluarga di rumah Hana." },
    { date: "Mei 2027", title: "Khitbah", body: "Keluarga Yusuf datang dari Dampit membawa hasil kebun kopi keluarga, dan dengan izin Allah lamaran diterima." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-21T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Ikhlas Dinoyo", address: "Jl. MT Haryono No. 12, Dinoyo, Kec. Lowokwaru, Kota Malang" },
    { name: "Walimah", date: "2027-08-21T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Gedung Serbaguna Graha Ijen", address: "Jl. Ijen No. 41, Oro-oro Dowo, Kec. Klojen, Kota Malang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7310 8821 05", account_name: "Hana Salsabila Putri" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "1440 0277 81", account_name: "Yusuf Abdurrahman Hakim" },
    { id: "demo-address", type: "address", address: "Jl. Kalpataru No. 18, Jatimulyo, Lowokwaru, Kota Malang 65141", account_name: "Keluarga H. Ahmad Syarifuddin" },
  ],
  guestName: "Ustadzah Rahmawati & Keluarga",
  guestTable: "Meja Karamel 2",
  extras: {
    quote: { text: "Ya Tuhan kami, anugerahkanlah kepada kami pasangan kami dan keturunan kami sebagai penyenang hati, dan jadikanlah kami pemimpin bagi orang-orang yang bertakwa.", source: "QS. Al-Furqan: 74" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah", note: "Area tamu putra & putri terpisah" },
      { time: "13.00", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim syar'i yang longgar. Nuansa krem, mocca, dan cokelat susu dipersilakan.", colors: ["#efe0cb", "#cfa57d", "#b97a45", "#6b4430"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar Abdul Hakim"] },
  },
});
