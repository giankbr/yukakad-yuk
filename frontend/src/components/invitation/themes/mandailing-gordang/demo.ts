import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Rizki",
    brideFull: "Siti Aisyah Lubis, S.E.", groomFull: "Rizki Fadillah Nasution, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak H. Mara Halim Lubis & Ibu Hj. Nur Asiah Harahap", groomParents: "Putra sulung dari\nBapak Sutan Parlindungan Nasution & Ibu Rosmaini Pulungan",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti sembilan gordang yang berbeda suara namun satu irama, semoga kami saling melengkapi dalam ridha Allah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Masjid Raya Al-Abror",
  address: "Jl. Masjid Raya, Wek I, Padangsidimpuan Utara, Kota Padangsidimpuan, Sumatera Utara",
  stories: [
    { date: "2021", title: "Bertemu di Sipirok", body: "Kami berkenalan di acara halalbihalal perantau Tapanuli Selatan. Aisyah membawa salak Sidimpuan, Rizki yang paling banyak menghabiskannya." },
    { date: "2025", title: "Lamaran", body: "Keluarga Rizki datang dengan adat dan doa. Dua keluarga bermusyawarah, hari baik pun ditetapkan." },
    { date: "2027", title: "Akad Nikah", body: "Dengan memohon rida Allah, kami melangkah bersama dengan restu kedua keluarga besar." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Raya Al-Abror", address: "Jl. Masjid Raya, Wek I, Padangsidimpuan Utara, Kota Padangsidimpuan" },
    { name: "Walimatul 'Ursy & Pesta Adat", date: "2027-07-11T10:00:00+07:00", time: "10.00 – 15.00 WIB", venue: "Aula Serbaguna Sipirok", address: "Jl. Sutan Soripada Mulia, Sipirok, Tapanuli Selatan" },
  ],
  gallery: ["/themes/img/r75.webp", "/themes/img/r74.webp", "/themes/img/r16.webp", "/themes/img/r14.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7166 2093 41", account_name: "Siti Aisyah Lubis" },
    { id: "demo-sumut", type: "bank", bank_name: "Bank Sumut Syariah", account_number: "611 02 04 009812 6", account_name: "Rizki Fadillah Nasution" },
  ],
  guestName: "Bapak H. Baginda Siregar & Keluarga",
  guestTable: "Meja Sopo 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "10.00", title: "Penyambutan tamu", note: "Diiringi gordang sambilan" },
      { time: "10.45", title: "Doa & kata sambutan keluarga" },
      { time: "11.30", title: "Makan bersama", note: "Gulai ikan sale dan sambal tuktuk" },
      { time: "13.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim resmi. Hijau, merah, dan hitam dipersilakan.", colors: ["#1f5a34", "#b02a26", "#1e1a16", "#f4f1e2"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-10T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Mara Halim Lubis", "Kel. Besar Sutan Parlindungan Nasution"] },
  },
});
