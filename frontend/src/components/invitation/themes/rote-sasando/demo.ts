import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Merlin", groom: "Yosua",
    brideFull: "Merlinda Agustina Henukh, S.Pd.", groomFull: "Yosua Imanuel Manafe, S.Kom.",
    brideParents: "Putri kedua dari\nBapak Daniel Henukh & Ibu Selfina Ndun", groomParents: "Putra sulung dari\nBapak Yeskiel Manafe & Ibu Marta Pah",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti dawai sasando yang berbeda nada namun dipetik dalam satu lagu, kami ingin saling melengkapi seumur hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T10:00:00+08:00",
  place: "GMIT Jemaat Imanuel Ba'a",
  address: "Jl. Kartini, Ba'a, Kecamatan Lobalain, Kabupaten Rote Ndao, Nusa Tenggara Timur",
  stories: [
    { date: "2020", title: "Petikan Pertama", body: "Yosua mengiringi paduan suara pemuda dengan sasando, Merlin bernyanyi di barisan sopran. Satu lagu, lalu banyak percakapan." },
    { date: "2024", title: "Senja di Nemberala", body: "Di pantai Nemberala, di bawah pohon lontar, Yosua bertanya dan Merlin menjawab ya." },
    { date: "2027", title: "Pemberkatan", body: "Dengan restu kedua keluarga dan berkat Tuhan, kami melangkah ke rumah tangga yang baru." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-17T10:00:00+08:00", time: "10.00 – 12.00 WITA", venue: "GMIT Jemaat Imanuel Ba'a", address: "Jl. Kartini, Ba'a, Lobalain, Kabupaten Rote Ndao, NTT" },
    { name: "Resepsi", date: "2027-07-24T18:00:00+08:00", time: "18.00 – 22.00 WITA", venue: "Balai Pertemuan Ina Boi", address: "Jl. Timor Raya No. 42, Oesapa, Kelapa Lima, Kota Kupang, NTT" },
  ],
  gallery: ["/themes/img/r15.webp", "/themes/img/r9.webp", "/themes/img/r110.webp", "/themes/img/r105.webp", "/themes/img/r103.webp"],
  gifts: [
    { id: "demo-bntt", type: "bank", bank_name: "Bank NTT", account_number: "021 01 07 118844 2", account_name: "Merlinda Agustina Henukh" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0533 01 024466 50 8", account_name: "Yosua Imanuel Manafe" },
    { id: "demo-kado", type: "address", address: "Jl. Kartini No. 9, Ba'a, Lobalain, Kabupaten Rote Ndao, NTT 85912" },
  ],
  guestName: "Bapak Pdt. Simon Lenggu & Keluarga",
  guestTable: "Meja Lontar 3",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "18.00", title: "Penyambutan tamu", note: "Diiringi petikan sasando" },
      { time: "18.30", title: "Doa & sambutan keluarga" },
      { time: "19.15", title: "Makan bersama" },
      { time: "20.00", title: "Foti & dansa bersama" },
    ] },
    dressCode: { note: "Busana resmi atau tenun ikat Rote. Topi ti'i langga untuk bapak-bapak sangat dipersilakan.", colors: ["#173447", "#2fb0ae", "#e2c07a", "#c8573a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-17T10:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Daniel Henukh", "Kel. Besar Yeskiel Manafe"] },
  },
});
