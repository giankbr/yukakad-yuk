import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sinta", groom: "Krisna",
    brideFull: "Ni Kadek Sinta Pradnyani, S.Par.", groomFull: "I Wayan Krisna Adinata, S.T.",
    brideParents: "Putri kedua dari\nBapak I Ketut Suardana & Ibu Ni Made Sukerti",
    groomParents: "Putra pertama dari\nBapak I Nyoman Adnyana & Ibu Ni Wayan Rasmini",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Kaktus tumbuh pelan di tanah yang kering, tapi selalu menemukan cara untuk berbunga. Begitu juga kami.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-05-22T09:00:00+08:00",
  place: "Padang Kaktus Garden, Pecatu",
  address: "Jl. Raya Uluwatu No. 88, Pecatu, Kuta Selatan, Kabupaten Badung, Bali",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Juni 2022", title: "Senja di Tebing", body: "Sinta memandu tur matahari terbenam di Uluwatu, Krisna salah satu pesertanya. Ia bertanya terlalu banyak tentang kaktus di pinggir tebing." },
    { date: "2023 – 2026", title: "Kebun Kecil Kami", body: "Kami mulai mengoleksi kaktus dan sukulen di teras rumah kos. Sekarang jumlahnya empat puluh tujuh pot, dan masing-masing punya nama." },
    { date: "Januari 2027", title: "Mapadik", body: "Keluarga Krisna datang secara resmi meminang Sinta. Kedua keluarga menentukan dewasa ayu untuk hari pawiwahan kami." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-05-22T09:00:00+08:00", time: "09.00 – 12.00 WITA", venue: "Kediaman Keluarga Mempelai Pria", address: "Banjar Kangin, Desa Pecatu, Kuta Selatan, Kabupaten Badung, Bali" },
    { name: "Resepsi", date: "2027-05-22T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Padang Kaktus Garden, Pecatu", address: "Jl. Raya Uluwatu No. 88, Pecatu, Kuta Selatan, Kabupaten Badung, Bali" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/r109.webp", "/themes/img/r105.webp", "/themes/img/a21.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "0110 2027 0522 01", account_name: "Ni Kadek Sinta Pradnyani" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0812 4477 15", account_name: "I Wayan Krisna Adinata" },
    { id: "demo-kado", type: "address", address: "Jl. Pantai Suluban Gg. Kaktus No. 3, Pecatu, Kuta Selatan, Badung, Bali 80361" },
  ],
  guestName: "Bli Gede Mahardika & Partner",
  guestTable: "Meja Saguaro 3",
  extras: {
    quote: { text: "Wahai pasangan suami-istri, semoga kalian tetap bersatu dan tidak pernah terpisahkan. Semoga kalian mencapai hidup yang penuh kebahagiaan, tinggal di rumah yang penuh kegembiraan bersama anak cucu.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Welcome drink & musik akustik" },
      { time: "17.45", title: "Senja bersama di taman kaktus" },
      { time: "18.30", title: "Santap malam", note: "Hidangan Bali & barbekyu" },
      { time: "20.00", title: "Api unggun & foto bersama" },
    ] },
    dressCode: { note: "Boho gurun: terakota, krem pasir, hijau sage, dan jingga senja. Sepatu datar disarankan, area taman berpasir.", colors: ["#c0643c", "#efd6b5", "#7f9a6e", "#e8875a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-22T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar I Ketut Suardana", "Kel. Besar I Nyoman Adnyana"] },
    wishlist: { items: [
      { id: "w1", name: "Pot terakota besar", price: "± Rp400.000" },
      { id: "w2", name: "Set kursi rotan teras", price: "± Rp2.000.000", claimed_by: "Teman kantor" },
      { id: "w3", name: "Tabungan rumah kebun", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah resepsi di ruang terbuka?", a: "Ya, di taman kaktus terbuka dengan pemandangan senja. Tersedia tenda bila hujan." },
      { q: "Bolehkah membawa anak?", a: "Tentu. Mohon awasi anak-anak di sekitar tanaman kaktus yang berduri." },
    ] },
  },
});
