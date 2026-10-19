import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Khadijah", groom: "Hamzah",
    note: "Di bawah langit yang sama, dua doa dipertemukan dalam satu ikatan suci.",
    brideFull: "Khadijah Nur Fadhilah, S.Pd.", groomFull: "Hamzah Al-Faruq, S.T.",
    brideParents: "Putri kedua dari Bapak H. Syamsul Arifin & Ibu Hj. Rahmawati",
    groomParents: "Putra pertama dari Bapak Drs. Ahmad Fauzi & Ibu Nurlaila",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-16T08:00:00+07:00",
  place: "Masjid Raya Al-Mashun",
  address: "Jl. Sisingamangaraja No. 61, Medan",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { title: "Ta'aruf", date: "2024", body: "Dikenalkan oleh guru mengaji kami, berawal dari satu majelis ilmu yang sama." },
    { title: "Istikharah", date: "2025", body: "Setelah saling mengenal dengan adab, kami memantapkan hati lewat doa dan restu orang tua." },
    { title: "Khitbah", date: "2026", body: "Hamzah datang bersama keluarga untuk meminang, disambut hangat oleh keluarga Khadijah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Al-Mashun", address: "Jl. Sisingamangaraja No. 61, Medan" },
    { name: "Walimatul 'Urs", date: "2027-05-16T19:30:00+07:00", time: "19.30 – 22.00 WIB", venue: "Taman Cahaya Ballroom", address: "Jl. Imam Bonjol No. 17, Medan" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/a86.webp", "/themes/img/a33.webp", "/themes/img/a139.webp", "/themes/img/a18.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7180 2233 4455", account_name: "Khadijah Nur Fadhilah" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 6655 4433", account_name: "Hamzah Al-Faruq" },
    { id: "demo-kado", type: "address", address: "Jl. Setia Budi No. 88, Tanjung Sari, Medan Selayang" },
  ],
  guestName: "Bapak H. Zulkifli & Keluarga",
  guestTable: "7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Ijab kabul", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "19.30", title: "Walimah dibuka", note: "Lantunan shalawat" },
      { time: "20.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim bernuansa malam: navy, emas, dan krem.", colors: ["#1a2550", "#f2c46d", "#efe6d2", "#5b4a7a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syamsul Arifin", "Kel. Besar Drs. Ahmad Fauzi", "Jamaah Majelis Taklim Nurul Iman"] },
    faq: { items: [
      { q: "Apakah tempat duduk tamu dipisah?", a: "Ya, tempat duduk walimah disediakan terpisah untuk tamu pria dan wanita." },
      { q: "Apakah tersedia tempat salat?", a: "Mushala tersedia di lantai dasar ballroom untuk salat Isya berjamaah." },
    ] },
  },
});
