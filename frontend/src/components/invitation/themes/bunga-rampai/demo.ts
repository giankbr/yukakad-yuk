import { makeDemo } from "../demo-base";

// Walimah syar'i tanpa foto di Medan: bunga rampai Melayu Deli (irisan pandan, mawar, melati, cempaka) dalam bokor kuningan.
export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Hafiz",
    brideFull: "Salma Khairunnisa, S.Farm.", groomFull: "Muhammad Hafiz Al-Ghifari, Lc.",
    brideParents: "Putri ketiga dari\nBapak H. Zulkarnain Nasution & Ibu Hj. Rahmah Lubis", groomParents: "Putra pertama dari\nBapak Drs. H. Syahrial & Ibu Nurhayati",
    note: "Seperti bunga rampai yang harum karena dirangkai bersama, semoga kami saling mengharumkan dalam ketaatan.",
  },
  eventLabel: "Walimatul 'Urs",
  date: "2027-06-19T09:00:00+07:00",
  place: "Gedung Serbaguna Pemprovsu",
  address: "Jl. Willem Iskandar, Medan Estate, Percut Sei Tuan, Deli Serdang",
  story: { title: "", body: "" },
  stories: [],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Al-Mashun", address: "Jl. Sisingamangaraja No. 61, Mesjid, Medan Kota, Medan" },
    { name: "Walimatul 'Urs", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Pemprovsu", address: "Jl. Willem Iskandar, Medan Estate, Percut Sei Tuan, Deli Serdang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7211 0456 89", account_name: "Salma Khairunnisa" },
    { id: "demo-kado", type: "address", address: "Jl. Karya Wisata No. 18, Gedung Johor, Medan Johor, Medan 20144" },
  ],
  guestName: "Ibu Hj. Fatimah Siregar & Keluarga",
  guestTable: "Melati 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Pembacaan ayat suci & tausiyah", note: "Ustadz H. Irwansyah Lubis" },
      { time: "11.40", title: "Tepung tawar & doa restu", note: "Tamu putra & putri terpisah" },
      { time: "12.15", title: "Jamuan makan siang" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Nuansa krem, merah mawar, dan hijau pandan.", colors: ["#f3e6d4", "#b44a5a", "#5f8a3a", "#c99a48"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkarnain Nasution", "Kel. Besar Drs. H. Syahrial"] },
    faq: { items: [
      { q: "Apakah tamu putra dan putri dipisah?", a: "Ya, ruang walimah dibagi dengan hijab untuk tamu putra dan putri." },
      { q: "Apakah ada musala?", a: "Tersedia musala dan tempat wudu di sayap timur gedung." },
    ] },
  },
});
