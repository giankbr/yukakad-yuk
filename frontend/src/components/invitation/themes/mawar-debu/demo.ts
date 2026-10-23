import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Ilyas",
    brideFull: "Nadhira Salsabila Rahmah, S.Psi.", groomFull: "Muhammad Ilyas Hanafi, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Fauzan & Ibu Hj. Nur Laila",
    groomParents: "Putra pertama dari\nBapak Drs. Hasan Basri & Ibu Rahmawati",
    note: "Seperti mawar yang dikeringkan dengan sabar, semoga cinta kami tetap utuh warnanya, lama setelah musim berganti.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-19T08:00:00+07:00",
  place: "Masjid Raya Al-Falah",
  address: "Jl. Raya Darmo No. 137A, Darmo, Wonokromo, Kota Surabaya",
  stories: [
    { date: "2024", title: "Majelis yang Sama", body: "Kami mengikuti kelas tahsin di masjid yang sama tanpa pernah bertegur sapa lebih dari salam." },
    { date: "2026", title: "Nadzor", body: "Melalui ustadzah pembimbing, keluarga kami dipertemukan dan kami saling mengenal dengan didampingi wali." },
    { date: "Maret 2027", title: "Khitbah", body: "Keluarga Ilyas datang bersilaturahmi membawa seikat mawar, dan dengan izin Allah lamaran diterima." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Al-Falah", address: "Jl. Raya Darmo No. 137A, Darmo, Wonokromo, Kota Surabaya" },
    { name: "Walimah", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Gedung Serbaguna Graha Sakinah", address: "Jl. Ketintang Baru Selatan I No. 22, Gayungan, Kota Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7203 1158 90", account_name: "Nadhira Salsabila Rahmah" },
    { id: "demo-address", type: "address", address: "Jl. Jemursari Selatan IV No. 9, Wonocolo, Surabaya 60237", account_name: "Keluarga H. Ahmad Fauzan" },
  ],
  guestName: "Ibu Hj. Maryam Khoirunnisa & Keluarga",
  guestTable: "Meja Mawar 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Nasihat pernikahan" },
      { time: "11.00", title: "Walimah", note: "Area tamu putra & putri terpisah" },
      { time: "13.00", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim syar'i yang longgar. Nuansa dusty rose, mauve, dan krem dipersilakan.", colors: ["#c9a3ad", "#8a6378", "#efe2dc", "#9a9878"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Fauzan", "Kel. Besar Drs. Hasan Basri"] },
  },
});
