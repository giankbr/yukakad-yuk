import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Agustina", groom: "Natalis",
    brideFull: "Agustina Maria Kayam, S.Pd.", groomFull: "Natalis Beorbit, S.Hut.",
    brideParents: "Putri kedua dari\nBapak Fransiskus Kayam & Ibu Theresia Amnemer", groomParents: "Putra sulung dari\nBapak Yosep Beorbit & Ibu Maria Yaam",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Sungai yang panjang membawa kami pulang ke satu dermaga. Kini kami mendayung bersama, searah dan seirama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T09:00:00+09:00",
  place: "Gereja Katedral Salib Suci Agats",
  address: "Jl. Yos Sudarso, Agats, Kabupaten Asmat, Papua Selatan",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Pesta Budaya Asmat", body: "Agustina memandu tamu di pameran ukiran, Natalis menjaga stan kelompok pengukir dari kampungnya. Kami berbincang lama di jalan papan depan museum." },
    { date: "2023", title: "Mengajar di Kampung", body: "Agustina mengajar di sekolah kampung di tepi sungai, Natalis mendampingi warga menanam sagu. Perahu mingguan jadi jadwal bertemu kami." },
    { date: "2027", title: "Satu Perahu", body: "Dengan restu keluarga besar dan berkat Tuhan, kami siap mendayung rumah tangga bersama." },
  ],
  events: [
    { name: "Misa Pemberkatan Nikah", date: "2027-10-09T09:00:00+09:00", time: "09.00 – 11.00 WIT", venue: "Gereja Katedral Salib Suci Agats", address: "Jl. Yos Sudarso, Agats, Kabupaten Asmat, Papua Selatan" },
    { name: "Resepsi & Makan Bersama", date: "2027-10-09T17:00:00+09:00", time: "17.00 – 21.00 WIT", venue: "Aula Keuskupan Agats", address: "Jl. Pemda I, Agats, Kabupaten Asmat, Papua Selatan" },
  ],
  gallery: ["/themes/img/r108.webp", "/themes/img/r89.webp", "/themes/img/r91.webp", "/themes/img/r90.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Papua", account_number: "2108 0331 4426", account_name: "Agustina Maria Kayam" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "7781 01 012245 53 9", account_name: "Natalis Beorbit" },
    { id: "demo-kado", type: "address", address: "Jl. Kompleks Misi No. 4, Agats, Kabupaten Asmat, Papua Selatan 99777" },
  ],
  guestName: "Bapak Paulus Tamot & Keluarga",
  guestTable: "Meja Sungai 2",
  extras: {
    quote: { text: "Berdua lebih baik daripada seorang diri. Dan tali tiga lembar tak mudah diputuskan.", source: "Pengkhotbah 4:9, 12" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Diiringi tifa dan nyanyian penyambutan" },
      { time: "17.45", title: "Doa syukur & sambutan keluarga" },
      { time: "18.30", title: "Makan bersama", note: "Sagu bakar, ikan bakar, dan papeda" },
      { time: "20.00", title: "Tari & foto bersama" },
    ] },
    dressCode: { note: "Busana rapi bernuansa kayu dan tanah: cokelat, putih kapur, merah oker, dan hitam.", colors: ["#4a2d1c", "#efe7d6", "#b0472b", "#1d1410"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Kayam – Amnemer", "Kel. Besar Beorbit – Yaam", "Umat Paroki Salib Suci Agats"] },
    travel: { note: "Agats adalah kota papan di atas rawa: jalan-jalannya berupa jembatan kayu dan beton.", items: [
      { name: "Dari Timika", detail: "Pesawat perintis ke Bandara Ewer, lalu speedboat ± 15 menit ke Agats" },
      { name: "Di dalam kota", detail: "Motor listrik atau jalan kaki di jalan papan, panitia siap menjemput dari dermaga" },
    ] },
  },
});
