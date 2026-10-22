import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Bayu",
    brideFull: "Larasati Kusuma Wardhani, S.Sn.", groomFull: "Bayu Adiwinata Rahman, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Slamet Riyadi & Ibu Hj. Sri Wulandari",
    groomParents: "Putra sulung dari\nBapak Drs. Abdul Rahman & Ibu Nurhayati",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Satu piringan hitam lawas, dua orang yang sama-sama mencarinya. Lagunya ternyata belum selesai diputar.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T08:00:00+07:00",
  place: "Rumah Nostalgia Menteng",
  address: "Jl. Cikini Raya No. 48, Menteng, Jakarta Pusat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Agustus 2022", title: "Rebutan Piringan Hitam", body: "Di sebuah lapak vinyl di Blok M, tangan kami meraih album yang sama. Bayu mengalah, Laras menawarinya mendengarkan bersama." },
    { date: "2023 – 2026", title: "Playlist Berdua", body: "Dari konser kecil di kafe sampai jalan-jalan sore naik vespa ke Kota Tua, setiap minggu kami menambah satu lagu ke daftar putar berdua." },
    { date: "Januari 2027", title: "Lamaran", body: "Bayu datang ke rumah keluarga Laras membawa seserahan dan piringan hitam yang dulu ia relakan, kini dengan cincin terselip di sampulnya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Cut Meutia", address: "Jl. Cut Meutia No. 1, Gondangdia, Menteng, Jakarta Pusat" },
    { name: "Resepsi", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Nostalgia Menteng", address: "Jl. Cikini Raya No. 48, Menteng, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a111.webp", "/themes/img/r85.webp", "/themes/img/a25.webp", "/themes/img/a126.webp", "/themes/img/r103.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "7310 4582 19", account_name: "Larasati Kusuma Wardhani" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1270 0091 4466 3", account_name: "Bayu Adiwinata Rahman" },
    { id: "demo-kado", type: "address", address: "Jl. Tebet Barat Dalam IV No. 12, Tebet, Jakarta Selatan 12810" },
  ],
  guestName: "Mas Andre & Partner",
  guestTable: "Meja Disko 7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Diiringi band lagu-lagu 70-an" },
      { time: "11.30", title: "Kirab pengantin & sambutan keluarga" },
      { time: "12.00", title: "Santap siang", note: "Es selendang mayang & kue jadul" },
      { time: "13.00", title: "Foto bersama di booth retro" },
    ] },
    dressCode: { note: "Gaya retro 70-an: jingga, kuning mustard, cokelat, dan krem. Motif bunga dan kacamata besar sangat dipersilakan.", colors: ["#e06a26", "#e9a632", "#5b3220", "#f4e4c1"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-12T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Slamet Riyadi", "Kel. Besar Drs. Abdul Rahman"] },
    wishlist: { items: [
      { id: "w1", name: "Pemutar piringan hitam", price: "± Rp2.500.000" },
      { id: "w2", name: "Set gelas kaca bermotif bunga", price: "± Rp450.000", claimed_by: "Geng SMA" },
      { id: "w3", name: "Tabungan bulan madu", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Wajib berbusana retro?", a: "Tidak wajib, tapi kami akan senang sekali. Ada booth foto bertema 70-an di lokasi." },
      { q: "Apakah tersedia parkir?", a: "Parkir terbatas. Kami sarankan naik KRL ke Stasiun Cikini lalu berjalan kaki 5 menit." },
    ] },
  },
});
