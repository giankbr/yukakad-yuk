import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Syifa", groom: "Hamzah",
    brideFull: "Syifa Nur Azizah, S.Farm.", groomFull: "Hamzah Abdullah Baraqbah, S.E.",
    brideParents: "Putri pertama dari\nBapak Ahmad Fauzi & Ibu Siti Khadijah", groomParents: "Putra ketiga dari\nBapak Umar Baraqbah & Ibu Fatimah Alaydrus",
    note: "Secangkir kopi yang dituang perlahan, sepiring kurma, dan majelis yang hangat: begitulah kami ingin menyambut setiap tamu di rumah tangga kami.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T09:00:00+07:00",
  place: "Gedung Al-Irsyad Surabaya",
  address: "Jl. Danakarya No. 46, Ampel, Semampir, Surabaya",
  stories: [
    { date: "2021", title: "Kedai Kopi di Ampel", body: "Hamzah menjaga kedai kopi milik keluarganya. Syifa datang setiap Jumat membeli kopi rempah untuk ayahnya." },
    { date: "2024", title: "Majelis Taklim", body: "Kami bertemu lagi di majelis taklim kampung. Orang tua kami ternyata sudah saling mengenal sejak lama." },
    { date: "2026", title: "Khitbah", body: "Keluarga Hamzah datang membawa kurma dan kopi terbaik. Lamaran diterima dengan senyum dan doa." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Sunan Ampel", address: "Jl. Ampel Masjid No. 53, Ampel, Semampir, Surabaya" },
    { name: "Walimah", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Al-Irsyad Surabaya", address: "Jl. Danakarya No. 46, Ampel, Semampir, Surabaya" },
  ],
  gallery: ["/themes/img/a23.webp", "/themes/img/a99.webp", "/themes/img/a18.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 2034 55", account_name: "Syifa Nur Azizah" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "1430 0567 21", account_name: "Hamzah Abdullah Baraqbah" },
    { id: "demo-kado", type: "address", address: "Jl. Nyamplungan Gg. V No. 9, Ampel, Semampir, Surabaya 60151" },
  ],
  guestName: "Bapak Ust. Salim Bawazier & Keluarga",
  guestTable: "Majelis 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Kopi rempah & kurma di majelis" },
      { time: "11.30", title: "Tausiyah pernikahan" },
      { time: "12.00", title: "Ramah tamah", note: "Nasi kebuli & gule kambing" },
      { time: "13.00", title: "Doa bersama & foto keluarga" },
    ] },
    dressCode: { note: "Busana muslim nuansa hangat: krem, cokelat kopi, kuningan, atau merah bata.", colors: ["#f3e6cc", "#5a3420", "#c4943e", "#9e2f24"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Ahmad Fauzi", "Kel. Besar Baraqbah", "Kel. Besar Alaydrus"] },
    faq: { items: [
      { q: "Apakah tempat tamu pria dan wanita dipisah?", a: "Ya, majelis tamu pria dan wanita disiapkan terpisah dengan pintu masuk masing-masing." },
      { q: "Apakah tersedia tempat salat?", a: "Tersedia musala di lantai dasar gedung, dan Masjid Ampel hanya lima menit berjalan kaki." },
    ] },
  },
});
