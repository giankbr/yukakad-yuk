import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hanifa", groom: "Ilham",
    brideFull: "Hanifa Az-Zahra, S.Ds.", groomFull: "Muhammad Ilham Ramadhan, S.Kom.",
    brideParents: "Putri kedua dari\nBapak H. Firdaus Hasan & Ibu Hj. Nurlaila", groomParents: "Putra pertama dari\nBapak Syamsul Bahri & Ibu Rahmawati",
    note: "Seperti kain yang diikat lalu dicelup, setiap simpul kesabaran meninggalkan pola yang indah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T09:00:00+07:00",
  place: "Gedung Serbaguna Masjid Agung",
  address: "Jl. Merdeka No. 1, 19 Ilir, Bukit Kecil, Kota Palembang",
  stories: [
    { date: "2021", title: "Bertemu di Majelis Ilmu", body: "Kami sama-sama menjadi panitia kajian remaja masjid dan saling mengenal lewat urusan konsumsi." },
    { date: "2026", title: "Ta'aruf", body: "Dengan perantara guru ngaji, kami bertukar biodata dan bertemu didampingi keluarga." },
    { date: "2027", title: "Khitbah & Akad", body: "Lamaran diterima dengan bahagia, dan kami memohon doa untuk hari akad." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Sultan Mahmud Badaruddin I", address: "Jl. Merdeka No. 1, 19 Ilir, Bukit Kecil, Kota Palembang" },
    { name: "Walimatul 'Ursy", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Masjid Agung", address: "Jl. Merdeka No. 1, 19 Ilir, Bukit Kecil, Kota Palembang", },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7180 2233 45", account_name: "Hanifa Az-Zahra" },
    { id: "demo-kado", type: "address", address: "Jl. Kebun Bunga Lr. Melati No. 9, Sukarami, Palembang 30152" },
  ],
  guestName: "Ibu Hj. Maryam & Keluarga",
  guestTable: "Meja Jumputan 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "09.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Tamu putra & putri terpisah" },
    ] },
    dressCode: { note: "Busana muslim warna pastel: merah muda, lilac, atau hijau toska.", colors: ["#e9a7b6", "#b9a6d8", "#86c6c0", "#fdf6ee"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Firdaus Hasan", "Kel. Besar Syamsul Bahri"] },
    faq: { items: [
      { q: "Apakah tamu putra dan putri dipisah?", a: "Ya, area walimah dipisah dengan tabir untuk kenyamanan bersama." },
      { q: "Apakah tersedia musala?", a: "Acara berlangsung di kompleks masjid, silakan salat Zuhur berjamaah." },
    ] },
  },
});
