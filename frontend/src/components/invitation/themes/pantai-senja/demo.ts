import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Damar",
    note: "Seperti ombak yang selalu pulang ke pantai, kami memilih untuk saling pulang.",
    brideFull: "Kirana Laut Prameswari, S.Ked.", groomFull: "Damar Samudra Wicaksono, S.T.",
    brideParents: "Putri kedua dari\nBapak Made Suarta & Ibu Luh Sekar Wangi", groomParents: "Putra sulung dari\nBapak Haris Wicaksono & Ibu Ratna Dewi",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T16:00:00+07:00",
  place: "Pantai Melasti, Ungasan",
  address: "Jl. Pantai Melasti, Ungasan, Kuta Selatan, Badung, Bali",
  stories: [
    { date: "2019", title: "Ombak pertama", body: "Bertemu di kelas selancar pagi di Kuta. Kirana jatuh dari papan, Damar yang pertama mengulurkan tangan." },
    { date: "2022", title: "Pulau demi pulau", body: "Dari Gili sampai Labuan Bajo, kami belajar bahwa perjalanan terbaik adalah yang dijalani berdua." },
    { date: "2026", title: "Di bawah langit jingga", body: "Saat matahari tenggelam di Uluwatu, Damar berlutut di atas pasir dan Kirana menjawab: iya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T16:00:00+07:00", time: "16.00 – 17.00 WITA", venue: "Tebing Pantai Melasti", address: "Jl. Pantai Melasti, Ungasan, Kuta Selatan, Badung, Bali" },
    { name: "Resepsi Senja", date: "2027-08-14T18:00:00+07:00", time: "18.00 – 21.00 WITA", venue: "Samudra Beach Club", address: "Jl. Pantai Melasti No. 8, Ungasan, Badung, Bali" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r15.webp", "/themes/img/r107.webp", "/themes/img/r12.webp", "/themes/img/r109.webp", "/themes/img/a21.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "7720 118 456", account_name: "Kirana Laut Prameswari" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 3456 7788", account_name: "Damar Samudra" },
    { id: "demo-kado", type: "address", address: "Jl. Tukad Badung No. 21, Renon, Denpasar Selatan, Bali" },
  ],
  guestName: "Bapak Wayan Sudarma & Keluarga",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "16.00", title: "Akad nikah", note: "Di tepi tebing, menghadap laut" },
      { time: "17.30", title: "Golden hour", note: "Foto bersama saat matahari terbenam" },
      { time: "18.00", title: "Resepsi senja dibuka" },
      { time: "19.30", title: "Makan malam & musik akustik" },
    ] },
    dressCode: { note: "Busana pantai yang santai dan rapi. Warna senja: koral, peach, krem. Sepatu datar disarankan.", colors: ["#e2725b", "#f6b98a", "#f8ecdc", "#3d5f8a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Made Suarta", "Kel. Besar Bpk. Haris Wicaksono"] },
    travel: { note: "Untuk tamu dari luar Bali, berikut beberapa info yang mungkin membantu.", items: [
      { name: "Shuttle dari Nusa Dua", detail: "Berangkat 15.00 WITA dari Bali Collection" },
      { name: "Penginapan terdekat", detail: "Kawasan Ungasan & Pecatu, ± 10 menit ke lokasi" },
    ] },
    faq: { items: [
      { q: "Apakah acara di area terbuka?", a: "Ya, akad di tebing terbuka dan resepsi di beach club semi terbuka. Bawa jaket tipis untuk malam hari." },
      { q: "Apakah tersedia parkir?", a: "Parkir tersedia di area atas Pantai Melasti, dengan shuttle golf car ke lokasi." },
    ] },
  },
});
