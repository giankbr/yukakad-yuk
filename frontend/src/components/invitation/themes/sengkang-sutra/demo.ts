import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahmah", groom: "Faisal",
    brideFull: "Andi Sitti Rahmah, S.E.", groomFull: "Andi Muh. Faisal Tenriawaru, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Andi Baso Patongai & Ibu Hj. Andi Bunga Walie", groomParents: "Putra sulung dari\nBapak H. Andi Mappasessu & Ibu Hj. Sitti Hasnah",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti benang sutra yang ditenun helai demi helai di Sengkang, semoga rumah tangga kami rapat, kuat, dan berkilau sepanjang usia.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T09:00:00+08:00",
  place: "Kompleks Rumah Adat Atakkae, Sengkang",
  address: "Kawasan Atakkae, Kec. Tempe, Kabupaten Wajo, Sulawesi Selatan",
  stories: [
    { date: "2018", title: "Di rumah tenun", body: "Rahmah membantu ibunya menenun lipa' sabbe. Faisal datang memesan sarung untuk acara keluarga, lalu kembali lagi dengan alasan yang terus berganti." },
    { date: "2022", title: "Senja di Danau Tempe", body: "Kami sering naik perahu ke rumah apung saat matahari turun, menunggu langit jingga memantul di air danau." },
    { date: "2026", title: "Mammanu'-manu'", body: "Keluarga Faisal datang menjajaki dengan santun. Setelah mappettuada, tanggal baik pun disepakati bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Agung Ummul Qura Sengkang", address: "Jl. Masjid Raya, Sengkang, Kec. Tempe, Kabupaten Wajo" },
    { name: "Resepsi (Tudang Botting)", date: "2027-08-14T11:30:00+08:00", time: "11.30 – 15.00 WITA", venue: "Kompleks Rumah Adat Atakkae", address: "Kawasan Atakkae, Kec. Tempe, Kabupaten Wajo" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a28.webp", "/themes/img/r109.webp", "/themes/img/a29.webp", "/themes/img/r38.webp", "/themes/img/r108.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Andi Sitti Rahmah" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0451 0100 2277 509", account_name: "Andi Muh. Faisal Tenriawaru" },
    { id: "demo-kado", type: "address", address: "Jl. Andi Ninnong No. 17, Sengkang, Kabupaten Wajo 90915" },
  ],
  guestName: "Bapak H. Andi Mappanyukki & Keluarga",
  guestTable: "Meja Tempe 5",
  extras: {
    rundown: { items: [
      { time: "11.30", title: "Mappasilukka' & sambutan keluarga" },
      { time: "12.00", title: "Tudang botting di pelaminan", note: "Diiringi kecapi dan gendang Bugis" },
      { time: "12.30", title: "Ramah tamah", note: "Nasu palekko, kapurung, dan barongko" },
      { time: "14.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Lipa' sabbe atau batik. Hijau giok, emas, dan krem dipersilakan.", colors: ["#0f625c", "#d6a43e", "#f1e3c2", "#c9573f"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar Patongai – Walie (Sengkang)", "Kel. Besar Mappasessu (Siwa, Wajo)"] },
  },
});
