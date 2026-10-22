import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahmi", groom: "Iqbal",
    brideFull: "Putri Rahmadhani, S.E.", groomFull: "Muhammad Iqbal Fauzan, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak H. Syamsul Bahri & Ibu Hj. Rosmaini", groomParents: "Putra kedua dari\nBapak Drs. H. Amri Yusuf & Ibu Hj. Fatimah Zahra",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Seperti sepasang angso yang berenang searah di Batanghari, semoga kami selalu seiring, setia, dan saling menjaga.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-18T08:30:00+07:00",
  place: "Gedung Pola Kantor Gubernur Jambi",
  address: "Jl. Jend. Ahmad Yani No. 1, Telanaipura, Kota Jambi",
  stories: [
    { date: "2019", title: "Kampus Mendalo", body: "Kami satu organisasi di Universitas Jambi. Rahmi bendahara yang teliti, Iqbal ketua panitia yang selalu terlambat menyerahkan nota." },
    { date: "2023", title: "Senja di Tanggo Rajo", body: "Di tepian Batanghari, sambil menunggu lampu Gentala Arasy menyala, Iqbal memberanikan diri bertanya tentang masa depan." },
    { date: "2026", title: "Lamaran", body: "Keluarga besar kami bertemu dan bersepakat dengan doa dan restu para tetua adat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Agung Al-Falah", address: "Jl. Sultan Thaha No. 60, Legok, Telanaipura, Kota Jambi" },
    { name: "Resepsi", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung Pola Kantor Gubernur Jambi", address: "Jl. Jend. Ahmad Yani No. 1, Telanaipura, Kota Jambi" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r16.webp", "/themes/img/r2.webp", "/themes/img/r109.webp"],
  gifts: [
    { id: "demo-jambi", type: "bank", bank_name: "Bank Jambi Syariah", account_number: "8012 3456 78", account_name: "Putri Rahmadhani" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7234 5678 90", account_name: "Muhammad Iqbal Fauzan" },
  ],
  guestName: "Ibu Hj. Nurhayati & Keluarga",
  guestTable: "Meja Angso 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Diiringi rebana dan pencak silat" },
      { time: "11.30", title: "Tari Sekapur Sirih", note: "Penyambutan tamu" },
      { time: "12.00", title: "Makan bersamo", note: "Gulai tepek ikan & nasi gemuk" },
    ] },
    dressCode: { note: "Busana muslim atau batik Jambi. Biru nila, merah sepang, dan kuning dipersilakan.", colors: ["#27365e", "#9b3a2a", "#d9a62e", "#f3e6c8"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T08:30:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syamsul Bahri", "Kel. Besar Drs. H. Amri Yusuf"] },
  },
});
