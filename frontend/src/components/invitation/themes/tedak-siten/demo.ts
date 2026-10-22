import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinan", groom: "",
    brideFull: "Kinanthi Ayu Prameswari",
    brideParents: "Putri pertama dari Bapak Wisnu Hadiprasetyo & Ibu Larasati Kusumaningrum",
    note: "Pitung lapan sudah Kinan lalui. Kini saatnya kaki mungilnya menapak bumi untuk pertama kali, dengan doa dan restu dari keluarga.",
  },
  eventLabel: "Tedak Siten",
  date: "2027-06-13T09:00:00+07:00",
  place: "Pendapa Omah Kebon",
  address: "Jl. Mondorakan No. 21, Prenggan, Kotagede, Yogyakarta",
  story: { title: "Bulan-bulan Pertama Kinan", body: "" },
  stories: [
    { date: "Oktober 2026", title: "Selamat datang, Kinan", body: "Lahir di Yogyakarta saat hujan pertama musim itu, dengan tangis kecil yang membuat seisi rumah tersenyum." },
    { date: "Desember 2026", title: "Senyum pertama", body: "Tersenyum lebar setiap mendengar Eyang Putri nembang dolanan sebelum tidur." },
    { date: "Maret 2027", title: "Tengkurap & berguling", body: "Mulai berguling ke sana kemari di atas tikar pandan, mengejar mainan kerincingan." },
    { date: "Mei 2027", title: "Duduk & merangkak", body: "Sekarang sudah bisa duduk sendiri dan merangkak menuju pintu, seolah tak sabar menapak keluar." },
  ],
  events: [
    { name: "Upacara Tedak Siten", date: "2027-06-13T09:00:00+07:00", time: "09.00 – 11.00 WIB", venue: "Pendapa Omah Kebon", address: "Jl. Mondorakan No. 21, Prenggan, Kotagede, Yogyakarta" },
    { name: "Kenduri & Ramah Tamah", date: "2027-06-13T11:00:00+07:00", time: "11.00 – 13.00 WIB", venue: "Pendapa Omah Kebon", address: "Jl. Mondorakan No. 21, Prenggan, Kotagede, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 3345 67", account_name: "Larasati Kusumaningrum" },
    { id: "demo-kado", type: "address", address: "Jl. Kemasan No. 9, Purbayan, Kotagede, Yogyakarta 55173" },
  ],
  guestName: "Ibu Sri Rahayu & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kinanthi Ayu Prameswari", nickname: "Kinan", birthDate: "2026-10-08T04:20:00+07:00", parents: "Putri pertama dari Bapak Wisnu Hadiprasetyo & Ibu Larasati Kusumaningrum", meaning: "Kinanthi: yang dituntun dengan kasih; Ayu Prameswari: cantik dan berbudi luhur." },
    rundown: { items: [
      { time: "09.00", title: "Sambutan keluarga & doa pembuka" },
      { time: "09.20", title: "Kinan menapaki jadah tujuh warna" },
      { time: "09.35", title: "Naik tangga tebu & ceker-ceker pasir" },
      { time: "09.50", title: "Masuk kurungan & memilih benda" },
      { time: "10.10", title: "Siraman kembang setaman & sebar udhik-udhik" },
      { time: "11.00", title: "Kenduri bersama" },
    ] },
    dressCode: { note: "Batik atau kebaya bernuansa pastel, sewarna jadah dan kembang setaman.", colors: ["#f3c1bd", "#f4dc94", "#a9c09f", "#c7b3d9", "#9cc0dc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Hadiprasetyo", "Eyang Kakung & Eyang Putri Kusumaningrum", "Pakde, Bude, Om & Tante sekeluarga"] },
    wishlist: { note: "Doa restu sudah lebih dari cukup. Bila ingin memberi, ini yang sedang Kinan butuhkan.", items: [
      { id: "w1", name: "Sepatu bayi pertama (ukuran 11 cm)", price: "± Rp150.000" },
      { id: "w2", name: "Buku kain bergambar", price: "± Rp90.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Baby walker kayu", price: "± Rp350.000" },
    ] },
    faq: { items: [
      { q: "Apa itu tedak siten?", a: "Upacara adat Jawa saat bayi berusia pitung lapan (7 × 35 hari), menandai pertama kali kakinya menapak tanah." },
      { q: "Boleh membawa anak kecil?", a: "Tentu. Anak-anak bisa ikut berebut udhik-udhik di akhir upacara." },
    ] },
  },
});
