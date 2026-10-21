import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahmi", groom: "Ferdi",
    brideFull: "Rahmi Ayu Pratiwi, S.E.", groomFull: "Ahmad Ferdiansyah, S.H.",
    brideParents: "Putri sulung dari\nBapak Drs. H. Bachtiar Basri gelar Suttan Pengiran & Ibu Hj. Nurhayati", groomParents: "Putra ketiga dari\nBapak H. Zulkarnain gelar Raja Pesirah & Ibu Hj. Rosmala Dewi",
    bridePhoto: "/themes/img/a62.webp", groomPhoto: "/themes/img/a60.webp",
    note: "Sai bumi ruwa jurai: dua keluarga, satu rumah, satu doa.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T08:00:00+07:00",
  place: "Gedung Serbaguna Way Halim",
  address: "Jl. Sultan Agung No. 12, Way Halim, Bandar Lampung",
  stories: [
    { date: "2018", title: "Festival Krakatau", body: "Kami berkenalan di barisan penari pembuka Festival Krakatau. Rahmi menari sigeh pengunten, Ferdi menabuh talo balak." },
    { date: "2022", title: "Merantau & Pulang", body: "Ferdi bekerja di Jakarta, Rahmi tetap di Bandar Lampung. Setiap mudik, kopi Lampung menjadi alasan untuk bertemu." },
    { date: "2026", title: "Nindai & Lamaran", body: "Keluarga Ferdi datang berkunjung secara adat. Dua jurai sepakat menyatukan kami." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Al-Furqon", address: "Jl. Diponegoro No. 1, Gulak Galik, Teluk Betung Utara, Bandar Lampung" },
    { name: "Resepsi Adat", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung Serbaguna Way Halim", address: "Jl. Sultan Agung No. 12, Way Halim, Bandar Lampung" },
  ],
  gallery: ["/themes/img/a62.webp", "/themes/img/a60.webp", "/themes/img/a61.webp", "/themes/img/a64.webp", "/themes/img/a18.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0213 4567 89", account_name: "Rahmi Ayu Pratiwi" },
    { id: "demo-kado", type: "address", address: "Jl. Pagar Alam No. 8, Kedaton, Bandar Lampung 35141" },
  ],
  guestName: "Bapak Hi. Syahril Effendi & Keluarga",
  guestTable: "Jurai 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Diiringi talo balak" },
      { time: "11.30", title: "Tari sigeh pengunten", note: "Tarian penyambutan tamu" },
      { time: "12.00", title: "Jamuan & ramah tamah" },
    ] },
    dressCode: { note: "Busana resmi atau bernuansa tapis. Merah tua, hitam, dan emas dipersilakan.", colors: ["#7e1620", "#1a0d0c", "#d1a648", "#efe2c4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Drs. H. Bachtiar Basri", "Kel. Besar H. Zulkarnain"] },
  },
});
