import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hanifa", groom: "Rasyid",
    brideFull: "Hanifa Nur Azizah, S.Pd.", groomFull: "Muhammad Rasyid Ilham, Lc.",
    brideParents: "Putri pertama dari\nBapak H. Abdul Ghofur & Ibu Hj. Siti Khotimah", groomParents: "Putra kedua dari\nBapak K.H. Masyhuri Ilham & Ibu Hj. Nur Laila",
    note: "Semoga Allah merajut hati kami seperti benang renda: halus, sabar, dan saling menguatkan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-24T08:00:00+07:00",
  place: "Grha Sabha Pramana UGM",
  address: "Jl. Pancasila, Bulaksumur, Sleman, Yogyakarta",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2024", title: "Pertemuan Dua Keluarga", body: "Ibunda kami dipertemukan dalam majelis taklim yang sama. Dari obrolan sederhana, lahir niat baik untuk saling mengenalkan putra-putrinya." },
    { date: "2026", title: "Khitbah", body: "Dengan bismillah, keluarga Rasyid datang mengkhitbah Hanifa di rumah Kotagede, disaksikan keluarga besar." },
    { date: "2027", title: "Akad Nikah", body: "Insyaallah kami menggenapkan separuh agama di hadapan Allah, keluarga, dan para sahabat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-24T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Gedhe Kauman", address: "Jl. Kauman, Ngupasan, Gondomanan, Yogyakarta" },
    { name: "Walimatul 'Ursy", date: "2027-04-24T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Grha Sabha Pramana UGM", address: "Jl. Pancasila, Bulaksumur, Sleman, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7221 0457 88", account_name: "Hanifa Nur Azizah" },
    { id: "demo-kado", type: "address", address: "Jl. Mondorakan No. 41, Kotagede, Yogyakarta 55173" },
  ],
  guestName: "Ibu Hj. Fatimah Zahra & Keluarga",
  guestTable: "Meja Melati 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu", note: "Tamu putra dan putri dipisah" },
      { time: "11.30", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "12.00", title: "Tausiyah pernikahan" },
      { time: "12.30", title: "Doa & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim/muslimah yang longgar dan sopan. Nuansa putih, gading, dan mauve dipersilakan.", colors: ["#fbf8f2", "#efe7da", "#a78a93", "#5d4a52"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Ghofur", "Kel. Besar K.H. Masyhuri Ilham"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, insyaallah tersedia area terpisah dengan hijab untuk tamu putra dan putri." },
      { q: "Apakah tersedia tempat salat?", a: "Tersedia musala di lantai dasar gedung." },
    ] },
  },
});
