import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Wira",
    brideFull: "Ni Luh Putu Ayu Wulandari, S.Pi.", groomFull: "I Made Agus Wiradana, S.T.",
    brideParents: "Putri pertama dari\nBapak I Wayan Sudarsana & Ibu Ni Ketut Sri Astuti",
    groomParents: "Putra kedua dari\nBapak I Nyoman Suarjana & Ibu Ni Made Rai Sumerti",
    note: "Kami bertemu di antara karang yang sedang tumbuh kembali. Seperti terumbu, cinta kami tumbuh perlahan, sabar, dan menjadi rumah bagi banyak kehidupan.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-08-21T09:00:00+08:00",
  place: "Bale Segara Sanur",
  address: "Jl. Pantai Mertasari No. 9, Sanur Kauh, Denpasar Selatan, Bali",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Transplantasi Karang", body: "Ayu memimpin relawan penanaman karang di Sanur. Wira datang sebagai penyelam relawan dan salah memasang rak karang terbalik di hari pertamanya." },
    { date: "2024", title: "Musim Bertelur", body: "Mereka begadang menunggu karang memijah di malam purnama. Malam itu Wira tahu ia ingin menunggu banyak purnama lagi bersama Ayu." },
    { date: "Februari 2027", title: "Memadik", body: "Keluarga Wira datang ke rumah keluarga Ayu untuk memadik, meminang dengan restu kedua keluarga besar." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-08-21T09:00:00+08:00", time: "09.00 – 12.00 WITA", venue: "Kediaman Mempelai Pria", address: "Br. Pekandelan, Sanur Kaja, Denpasar Selatan, Bali" },
    { name: "Resepsi", date: "2027-08-21T18:00:00+08:00", time: "18.00 – 21.00 WITA", venue: "Bale Segara Sanur", address: "Jl. Pantai Mertasari No. 9, Sanur Kauh, Denpasar Selatan, Bali" },
  ],
  gallery: ["/themes/img/r11.webp", "/themes/img/r110.webp", "/themes/img/r103.webp", "/themes/img/r5.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "018 02 11 54321 7", account_name: "Ni Luh Putu Ayu Wulandari" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0938 4471 26", account_name: "I Made Agus Wiradana" },
    { id: "demo-kado", type: "address", address: "Br. Pekandelan, Jl. Danau Poso No. 31, Sanur Kaja, Denpasar Selatan, Bali 80228" },
  ],
  guestName: "Bapak I Ketut Arsana & Keluarga",
  guestTable: "Meja Terumbu 2",
  extras: {
    quote: { text: "Tetaplah kalian berdua di sini, jangan pernah terpisahkan. Nikmatilah seluruh usia bersama putra dan cucu, bersukacita di rumah kalian sendiri.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "18.00", title: "Penyambutan tamu", note: "Taman tepi pantai" },
      { time: "18.30", title: "Tari penyambutan & doa bersama" },
      { time: "19.00", title: "Santap malam", note: "Hidangan laut & masakan Bali" },
      { time: "20.30", title: "Foto bersama keluarga & sahabat" },
    ] },
    dressCode: { note: "Busana adat madya atau nuansa biru laut, toska, dan pasir. Tamu wanita dipersilakan berkebaya.", colors: ["#0d3a63", "#1f7f9e", "#7cc9d0", "#e9d6a8"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-21T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. I Wayan Sudarsana", "Kel. Besar Bpk. I Nyoman Suarjana"] },
    travel: { note: "Untuk tamu dari luar Bali, berikut pilihan menginap di sekitar Sanur.", items: [
      { name: "Penginapan di kawasan Mertasari", detail: "± 500 m dari Bale Segara" },
      { name: "Dari Bandara Ngurah Rai", detail: "± 30 menit berkendara lewat jalan tol Bali Mandara" },
    ] },
    wishlist: { items: [
      { id: "w1", name: "Perlengkapan selam untuk berdua", price: "± Rp2.500.000" },
      { id: "w2", name: "Donasi adopsi karang", price: "± Rp250.000", claimed_by: "Bli Komang" },
      { id: "w3", name: "Tabungan rumah pertama", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah tamu wajib berbusana adat?", a: "Tidak wajib. Busana adat madya sangat dihargai, busana rapi juga dipersilakan." },
      { q: "Apakah tersedia parkir?", a: "Parkir tersedia di area Pantai Mertasari, dengan petugas yang mengarahkan." },
    ] },
  },
});
