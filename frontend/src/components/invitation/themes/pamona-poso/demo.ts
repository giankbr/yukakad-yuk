import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Debora", groom: "Yosua",
    brideFull: "Debora Ninggeng Tarante, S.Kep.", groomFull: "Yosua Pratama Lasampa, S.Hut.",
    brideParents: "Putri ketiga dari\nBapak Pdt. Markus Tarante & Ibu Ester Pelima", groomParents: "Putra sulung dari\nBapak Daniel Lasampa & Ibu Ribka Tampake",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti Danau Poso yang jernih sampai ke dasarnya, kami ingin saling terbuka dan setia, mengalir bersama seperti sungai yang keluar dari danau.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-26T10:00:00+08:00",
  place: "Gereja GKST Jemaat Eklesia Tentena",
  address: "Jl. Pulau Sumatera No. 4, Kel. Tentena, Kec. Pamona Puselemba, Kabupaten Poso",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2018", title: "Festival Danau Poso", body: "Kami bertemu sebagai panitia festival. Debora mengurus tamu, Yosua mengatur perahu yang membawa tamu menyeberang ke Siuri." },
    { date: "2022", title: "Sore di Jembatan Tua", body: "Setiap pulang kerja kami berjalan di jembatan kayu Pamona, melihat orang memasang wayamasapi di arus sungai sambil bercerita tentang masa depan." },
    { date: "2026", title: "Lamaran Adat", body: "Keluarga Lasampa datang meminang dengan membawa tanda adat Pamona. Kedua keluarga bersepakat dengan doa dan sukacita." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-06-26T10:00:00+08:00", time: "10.00 – 12.00 WITA", venue: "Gereja GKST Jemaat Eklesia Tentena", address: "Jl. Pulau Sumatera No. 4, Kel. Tentena, Kec. Pamona Puselemba, Kabupaten Poso" },
    { name: "Resepsi Pernikahan", date: "2027-06-26T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Dodoha Mosintuwu", address: "Jl. Yos Sudarso, tepi Danau Poso dekat Jembatan Pamona, Tentena, Kabupaten Poso" },
  ],
  gallery: ["/themes/img/a33.webp", "/themes/img/r108.webp", "/themes/img/r104.webp", "/themes/img/a30.webp", "/themes/img/r109.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0451 0100 7782 506", account_name: "Debora Ninggeng Tarante" },
    { id: "demo-sulteng", type: "bank", bank_name: "Bank Sulteng", account_number: "006 01 22 013458", account_name: "Yosua Pratama Lasampa" },
    { id: "demo-kado", type: "address", address: "Jl. Danau Poso No. 17, Kel. Pamona, Kec. Pamona Puselemba, Kabupaten Poso 94663" },
  ],
  guestName: "Bapak Yohanis Kalengke & Keluarga",
  guestTable: "Meja Siuri 2",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Diiringi musik bambu dan tarian Dero pembuka" },
      { time: "17.45", title: "Kedatangan kedua mempelai", note: "Mengenakan busana adat Pamona bermanik" },
      { time: "18.30", title: "Doa dan makan bersama", note: "Ikan sogili bakar dan nasi bambu" },
      { time: "19.30", title: "Dero bersama", note: "Tarian melingkar, semua tamu diajak bergandeng tangan" },
    ] },
    dressCode: { note: "Batik atau busana bernuansa biru danau, putih pasir, dan aksen manik merah-kuning.", colors: ["#1f6f78", "#f3ecdd", "#b8322a", "#e0a52a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-26T10:00:00+08:00" },
    rsvpDietary: {},
    family: { names: ["Kel. Besar Tarante – Pelima", "Kel. Besar Lasampa – Tampake", "Majelis Jemaat GKST Eklesia Tentena"] },
    travel: { note: "Tentena dapat dicapai dari Bandara Kasiguncu Poso (± 1,5 jam) atau dari Palu lewat jalan darat (± 7 jam).", items: [
      { name: "Penginapan tepi danau", detail: "Banyak penginapan di sekitar Jembatan Pamona, ± 5 menit dari gereja" },
      { name: "Pantai Siuri", detail: "Bagi tamu yang menginap, keluarga mengajak berenang di pasir putih Siuri pada Minggu pagi" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh ikut menari Dero?", a: "Tentu. Dero adalah tarian kebersamaan, semua tamu diajak bergandeng tangan dalam lingkaran." },
      { q: "Apakah ada parkir di Dodoha?", a: "Ada, parkir tersedia di halaman Dodoha dan sepanjang Jl. Yos Sudarso." },
    ] },
  },
});
