import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "",
    brideFull: "Raden Rara Larasati Ayuningtyas, S.Psi.",
    brideParents: "Putri kedua dari Bapak Bambang Suryo Atmojo & Ibu Endang Sri Rejeki",
    note: "Sehari sebelum ijab, Laras akan disucikan dengan air kembang setaman dari tujuh sumber, diiringi doa para pinisepuh.",
  },
  eventLabel: "Siraman",
  date: "2027-07-09T10:00:00+07:00",
  place: "Dalem Atmajan",
  address: "Jl. Gajahan No. 14, Baluwarti, Pasar Kliwon, Surakarta",
  story: { title: "", body: "" },
  stories: [],
  events: [
    { name: "Sungkeman & Siraman", date: "2027-07-09T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "Pelataran Dalem Atmajan", address: "Jl. Gajahan No. 14, Baluwarti, Pasar Kliwon, Surakarta" },
    { name: "Midodareni", date: "2027-07-09T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Pendapa Dalem Atmajan", address: "Jl. Gajahan No. 14, Baluwarti, Pasar Kliwon, Surakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0921 0100 4471 509", account_name: "Endang Sri Rejeki" },
    { id: "demo-kado", type: "address", address: "Jl. Gajahan No. 14, Baluwarti, Pasar Kliwon, Surakarta 57144" },
  ],
  guestName: "Ibu Sri Lestari & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Raden Rara Larasati Ayuningtyas, S.Psi.", nickname: "Laras", parents: "Putri kedua dari Bapak Bambang Suryo Atmojo & Ibu Endang Sri Rejeki", meaning: "Larasati: yang selaras; Ayuningtyas: elok hatinya." },
    rundown: { items: [
      { time: "10.00", title: "Sungkeman kepada Bapak & Ibu" },
      { time: "10.20", title: "Siraman oleh tujuh pinisepuh", note: "Diawali Bapak, ditutup Ibu" },
      { time: "11.00", title: "Wudhu dari kendi & pecah kendi" },
      { time: "11.15", title: "Potong rikma & tanam rikma" },
      { time: "11.30", title: "Dodol dawet", note: "Tamu membeli dawet dengan kreweng" },
    ] },
    dressCode: { note: "Kebaya atau batik bernuansa hijau pupus, gading, dan merah muda kembang.", colors: ["#a9c79a", "#f3ecd2", "#e7a7a9", "#6f9a7a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Atmojo", "Keluarga Besar Trah Sastrowiyono", "Pakde, Bude, Om & Tante sekeluarga"] },
    faq: { items: [
      { q: "Apa itu siraman?", a: "Upacara memandikan calon pengantin dengan air kembang setaman sehari sebelum ijab, sebagai lambang penyucian lahir dan batin." },
      { q: "Bolehkah tamu ikut dodol dawet?", a: "Tentu. Kreweng (pecahan tembikar) disediakan di meja penerima tamu untuk membeli dawet." },
    ] },
  },
});
