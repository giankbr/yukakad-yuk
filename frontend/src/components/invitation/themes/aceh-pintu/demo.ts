import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Rizki",
    brideFull: "Cut Nadia Safira, S.Ked.", groomFull: "Teuku Muhammad Rizki, S.T.",
    brideParents: "Putri sulung dari\nBapak Teuku H. Banta Ahmad & Ibu Cut Hj. Rosmawati", groomParents: "Putra kedua dari\nBapak Tgk. H. Abdullah Yusuf & Ibu Hj. Nurlaila",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Semoga Allah menjadikan rumah kami sakinah, mawaddah, wa rahmah, dan pintunya selalu terbuka bagi keluarga dan sahabat.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-17T09:00:00+07:00",
  place: "Gedung AAC Dayan Dawood",
  address: "Jl. Teuku Nyak Arief, Kopelma Darussalam, Syiah Kuala, Banda Aceh",
  stories: [
    { date: "2019", title: "Kampus Darussalam", body: "Kami satu angkatan di Universitas Syiah Kuala dan sering berjumpa di perpustakaan menjelang ujian." },
    { date: "2024", title: "Ba Ranub", body: "Keluarga Rizki datang membawa sirih (ba ranub) sebagai tanda lamaran. Keluarga Nadia menerimanya dengan doa." },
    { date: "2027", title: "Hari yang Dinanti", body: "Dengan izin Allah, kami melangkah ke jenjang pernikahan di Banda Aceh." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Raya Baiturrahman", address: "Jl. Moh. Jam No. 1, Kampung Baru, Baiturrahman, Banda Aceh" },
    { name: "Walimatul 'Ursy", date: "2027-04-17T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung AAC Dayan Dawood", address: "Jl. Teuku Nyak Arief, Kopelma Darussalam, Syiah Kuala, Banda Aceh" },
  ],
  gallery: ["/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a116.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Cut Nadia Safira" },
    { id: "demo-aceh", type: "bank", bank_name: "Bank Aceh Syariah", account_number: "010 01 02 345678 9", account_name: "Teuku Muhammad Rizki" },
  ],
  guestName: "Bapak Tgk. Zulfikar & Keluarga",
  guestTable: "Meja 7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Intat linto baro", note: "Rombongan mempelai pria tiba" },
      { time: "11.30", title: "Peusijuek", note: "Tepung tawar oleh para sesepuh" },
      { time: "12.00", title: "Jamuan & ramah tamah", note: "Kuah beulangong" },
    ] },
    dressCode: { note: "Busana muslim. Hitam, merah, hijau, dan kuning keemasan dipersilakan.", colors: ["#121010", "#b8262a", "#2f7a3c", "#e2b337"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-04-17T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Teuku H. Banta Ahmad", "Kel. Besar Tgk. H. Abdullah Yusuf"] },
  },
});
