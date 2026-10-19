import { makeDemo } from "../demo-base";

// Bugis-Makassar: mappacci (malam pacar) → akad nikah → tudang botting (resepsi) → mapparola.
export const demo = makeDemo({
  couple: {
    bride: "Tenri", groom: "Fadli",
    brideFull: "Andi Tenri Ajeng Pratiwi, S.Farm.", groomFull: "Muhammad Fadli Mappiare, S.H.",
    brideParents: "Putri dari\nBapak H. Andi Mappasessu & Ibu Hj. Andi Nurhayati", groomParents: "Putra dari\nBapak H. Abdul Rahman Daeng Sila & Ibu Hj. St. Aisyah",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T09:00:00+08:00",
  place: "Baruga Lompoa Convention Hall",
  address: "Jl. Jenderal Sudirman No. 45, Ujung Pandang, Kota Makassar",
  stories: [
    { date: "2019", title: "Bertemu di Losari", body: "Kenalan tanpa sengaja saat buka puasa bersama teman kampus di Pantai Losari. Pisang epe jadi saksi." },
    { date: "2023", title: "Saling Menjaga", body: "Empat tahun bersama, melewati kuliah profesi Tenri dan sumpah advokat Fadli." },
    { date: "2026", title: "Mappettu Ada", body: "Keluarga Fadli datang melamar. Dua keluarga sepakat menentukan hari baik dan uang panai'." },
  ],
  events: [
    { name: "Mappacci", date: "2027-08-20T19:30:00+08:00", time: "19.30 WITA – selesai", venue: "Kediaman Mempelai Wanita", address: "Jl. Gunung Bawakaraeng No. 17, Makassar" },
    { name: "Akad Nikah", date: "2027-08-21T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Raya Makassar", address: "Jl. Masjid Raya No. 57, Bontoala, Kota Makassar" },
    { name: "Tudang Botting (Resepsi)", date: "2027-08-21T19:00:00+08:00", time: "19.00 – 22.00 WITA", venue: "Baruga Lompoa Convention Hall", address: "Jl. Jenderal Sudirman No. 45, Ujung Pandang, Kota Makassar" },
    { name: "Mapparola", date: "2027-08-22T10:00:00+08:00", time: "10.00 WITA", venue: "Kediaman Mempelai Pria", address: "Jl. Perintis Kemerdekaan Km. 9, Tamalanrea, Makassar" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/r64.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/r10.webp", "/themes/img/r12.webp", "/themes/img/r109.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Andi Tenri Ajeng Pratiwi" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "152 00 1234567 8", account_name: "Muhammad Fadli Mappiare" },
    { id: "demo-kado", type: "address", address: "Jl. Gunung Bawakaraeng No. 17, Makassar 90157" },
  ],
  guestName: "Bapak Andi Baso & Keluarga",
  guestTable: "5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.00", title: "Tamu tiba", note: "Disambut keluarga & pa'baju bodo" },
      { time: "19.30", title: "Tudang botting", note: "Mempelai duduk di lamming" },
      { time: "20.00", title: "Ramah tamah & santap malam" },
      { time: "21.30", title: "Foto bersama", note: "Per rombongan keluarga" },
    ] },
    dressCode: { note: "Warna cerah dipersilakan. Baju bodo atau lipa' sabbe akan sangat istimewa.", colors: ["#c2185b", "#0f7a5c", "#ef7d22", "#d4a532"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-21T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Keluarga Besar H. Andi Mappasessu", "Keluarga Besar H. Abdul Rahman Daeng Sila", "Kerukunan Keluarga Bone di Makassar"] },
    travel: { note: "Untuk keluarga dari luar daerah, berikut beberapa pilihan terdekat.", items: [
      { name: "Hotel di sekitar Pantai Losari", detail: "± 2 km dari gedung" },
      { name: "Parkir gedung", detail: "Tersedia parkir mobil & motor" },
    ] },
    faq: { items: [
      { q: "Apakah mappacci terbuka untuk tamu?", a: "Mappacci adalah malam keluarga; tamu undangan khusus dipersilakan hadir di kediaman mempelai wanita." },
      { q: "Apakah tersedia parkir?", a: "Ada parkir luas di area gedung." },
    ] },
  },
});
