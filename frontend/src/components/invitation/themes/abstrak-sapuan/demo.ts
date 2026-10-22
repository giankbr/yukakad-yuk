import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Saraswati", groom: "Arya",
    brideFull: "Ni Luh Putu Saraswati Dewi, S.Sn.", groomFull: "I Gede Arya Wibawa, M.Ds.",
    brideParents: "Putri pertama dari\nBapak I Wayan Sudarsana & Ibu Ni Made Rai Astuti", groomParents: "Putra kedua dari\nBapak I Ketut Wibawa & Ibu Ni Nyoman Sukerti",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Dua kuas, satu kanvas. Kami memutuskan untuk melukis babak berikutnya bersama.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-08-14T10:00:00+08:00",
  place: "Ruang Sapuan, Ubud",
  address: "Jl. Raya Sanggingan No. 27, Kedewatan, Ubud, Gianyar, Bali",
  stories: [
    { date: "Maret 2022", title: "Residensi Seni di Ubud", body: "Saras melukis bidang-bidang warna di studio sebelah. Arya, perancang pameran, datang meminjam selotip kertas dan tak kunjung pulang." },
    { date: "2024", title: "Pameran Pertama Berdua", body: "Delapan kanvas besar, satu ruang putih, dan obrolan panjang tentang warna ochre yang tak pernah selesai." },
    { date: "Januari 2027", title: "Ngidih & Mepadik", body: "Keluarga besar Arya datang meminang ke rumah keluarga Saras di Gianyar, disambut restu kedua belah pihak." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-08-14T10:00:00+08:00", time: "10.00 – 13.00 WITA", venue: "Kediaman Keluarga Mempelai Pria", address: "Banjar Kutuh Kaja, Desa Petulu, Ubud, Gianyar, Bali" },
    { name: "Resepsi di Galeri", date: "2027-08-14T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Ruang Sapuan, Ubud", address: "Jl. Raya Sanggingan No. 27, Kedewatan, Ubud, Gianyar, Bali" },
  ],
  gallery: ["/themes/img/r88.webp", "/themes/img/a123.webp", "/themes/img/a101.webp", "/themes/img/r72.webp", "/themes/img/a122.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "0180 2026 7731", account_name: "Ni Luh Putu Saraswati Dewi" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "1288 4417 05", account_name: "I Gede Arya Wibawa" },
    { id: "demo-kado", type: "address", address: "Jl. Bisma No. 12, Ubud, Gianyar, Bali 80571" },
  ],
  guestName: "Bapak Komang Adi Pranata & Keluarga",
  guestTable: "Meja Ochre 2",
  extras: {
    quote: { text: "Tetaplah kalian berdua di sini, jangan pernah terpisahkan. Nikmatilah umur panjang, bermain dan bersukacita bersama putra dan cucu, berbahagia di rumah kalian sendiri.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "17.00", title: "Pembukaan pameran & sambutan tamu", note: "Minuman di teras galeri" },
      { time: "17.45", title: "Kedua mempelai memasuki ruang pamer" },
      { time: "18.15", title: "Sapuan bersama", note: "Satu kanvas besar untuk dilukis semua tamu" },
      { time: "19.00", title: "Santap malam & musik akustik" },
    ] },
    dressCode: { note: "Netral dan lembut seperti ruang galeri: krem, blush, sage, ochre, atau arang. Busana adat madya dipersilakan.", colors: ["#e4ac9c", "#a3b398", "#cf973f", "#2d2b2a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. I Wayan Sudarsana", "Kel. Besar Bpk. I Ketut Wibawa", "Kolektif Seniman Ruang Sapuan"] },
    travel: { note: "Ubud ramai di akhir pekan. Mohon datang lebih awal dan gunakan area parkir galeri.", items: [
      { name: "Parkir", detail: "Lapangan Kedewatan, 200 m dari galeri, ada pengantar" },
      { name: "Menginap", detail: "Beberapa vila di Sanggingan, kode tamu SAPUAN" },
    ] },
  },
});
