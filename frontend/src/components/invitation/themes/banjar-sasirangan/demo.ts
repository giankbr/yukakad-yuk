import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aulia", groom: "Hafiz",
    brideFull: "Noor Aulia Rahmah, S.Pd.", groomFull: "Muhammad Hafiz Ridhani, S.Hut.",
    brideParents: "Putri bungsu dari\nBapak H. Abdul Hadi & Ibu Hj. Siti Mariam", groomParents: "Putra sulung dari\nBapak H. Gusti Syahrani & Ibu Hj. Noorhayati",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti jukung yang berlayar seiring arus Martapura, semoga kami selalu sejalan menuju rida-Nya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+08:00",
  place: "Gedung Mahligai Pancasila",
  address: "Jl. Jenderal Sudirman No. 14, Antasan Besar, Banjarmasin Tengah, Banjarmasin",
  stories: [
    { date: "2018", title: "Pasar Terapung", body: "Pagi-pagi di pasar terapung Lok Baintan, jukung kami bersenggolan. Satu sisir pisang jatuh ke sungai dan Hafiz yang memungutnya." },
    { date: "2022", title: "Kain Sasirangan", body: "Aulia belajar mencelup sasirangan di Kampung Sasirangan; Hafiz menjadi pembeli pertamanya yang paling setia." },
    { date: "2026", title: "Basasuluh & Bapapayuan", body: "Keluarga Hafiz datang melamar secara adat Banjar. Dua keluarga bermufakat menentukan hari baik." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+08:00", time: "08.00 – 09.30 WITA", venue: "Masjid Raya Sabilal Muhtadin", address: "Jl. Jenderal Sudirman No. 1, Antasan Besar, Banjarmasin Tengah" },
    { name: "Resepsi", date: "2027-08-14T11:00:00+08:00", time: "11.00 – 15.00 WITA", venue: "Gedung Mahligai Pancasila", address: "Jl. Jenderal Sudirman No. 14, Antasan Besar, Banjarmasin Tengah" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a18.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bankkalsel", type: "bank", bank_name: "Bank Kalsel", account_number: "0012 0345 6789", account_name: "Noor Aulia Rahmah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7234 5678 90", account_name: "Muhammad Hafiz Ridhani" },
  ],
  guestName: "Bapak H. Rusdiansyah & Keluarga",
  guestTable: "Meja 9",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan bausung", note: "Diiringi sinoman hadrah" },
      { time: "11.30", title: "Sambutan keluarga" },
      { time: "12.00", title: "Jamuan", note: "Soto Banjar & wadai" },
    ] },
    dressCode: { note: "Busana muslim atau kain sasirangan. Hijau, kuning, dan merah marun dipersilakan.", colors: ["#2f6b3a", "#e3b23c", "#7a1f2b", "#f5eedc"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Hadi", "Kel. Besar H. Gusti Syahrani"] },
  },
});
