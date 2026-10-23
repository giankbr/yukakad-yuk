import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nayla", groom: "Haikal",
    brideFull: "Nayla Azzahra Mahmud, S.Farm.", groomFull: "Haikal Rasyid Pallawa, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak H. Mahmud Daeng Situju & Ibu Hj. Sitti Aminah",
    groomParents: "Putra kedua dari\nBapak Ir. Rasyid Pallawa & Ibu Andi Nurhayati",
    note: "Di bawah langit yang sama kami berdoa dalam diam, lalu Allah mempertemukan doa itu pada waktu yang paling baik.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-11T09:00:00+08:00",
  place: "Masjid Al-Markaz Al-Islami",
  address: "Jl. Mesjid Raya No. 57, Bontoala, Kota Makassar, Sulawesi Selatan",
  stories: [
    { date: "2025", title: "Satu Rombongan Umrah", body: "Keluarga kami berangkat dalam rombongan yang sama. Kami hanya saling tahu nama dari daftar jamaah." },
    { date: "2026", title: "Ta'aruf", body: "Sepulang umrah, orang tua kami bersilaturahmi. Kami bertukar biodata dan bertemu didampingi keluarga." },
    { date: "Juni 2027", title: "Mappettuada", body: "Lamaran disampaikan dengan adat yang sederhana, dan dengan izin Allah kedua keluarga bersepakat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Al-Markaz Al-Islami", address: "Jl. Mesjid Raya No. 57, Bontoala, Kota Makassar, Sulawesi Selatan" },
    { name: "Walimah", date: "2027-09-11T19:30:00+08:00", time: "19.30 – 21.30 WITA", venue: "Ballroom Hotel Claro", address: "Jl. A. P. Pettarani No. 3, Mannuruki, Tamalate, Kota Makassar" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7166 0425 18", account_name: "Nayla Azzahra Mahmud" },
    { id: "demo-bank2", type: "bank", bank_name: "BNI", account_number: "0883 2716 54", account_name: "Haikal Rasyid Pallawa" },
  ],
  guestName: "Bapak H. Syamsul Bahri & Keluarga",
  guestTable: "Meja Bintang 5",
  extras: {
    quote: { text: "Maha Suci Allah yang telah menciptakan pasangan-pasangan semuanya, baik dari apa yang ditumbuhkan oleh bumi dan dari diri mereka sendiri, maupun dari apa yang tidak mereka ketahui.", source: "QS. Yasin: 36" },
    rundown: { items: [
      { time: "09.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Tausiyah & doa" },
      { time: "19.30", title: "Walimah", note: "Area tamu putra & putri terpisah" },
      { time: "21.00", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim syar'i. Nuansa biru tua, abu perak, atau putih dipersilakan.", colors: ["#13254a", "#cdd4de", "#f4f6fa", "#3b5d93"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Mahmud Daeng Situju", "Kel. Besar Ir. Rasyid Pallawa"] },
  },
});
