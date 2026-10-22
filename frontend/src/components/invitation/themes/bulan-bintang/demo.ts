import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nabila", groom: "Faris",
    brideFull: "Nabila Qonita Azzahra", groomFull: "Muhammad Faris Al-Hakim",
    brideParents: "Putri kedua dari\nBapak H. Syamsul Bahri & Ibu Hj. Rosmawati", groomParents: "Putra pertama dari\nBapak Drs. Abdul Latif & Ibu Siti Khadijah",
    note: "Seperti bulan yang tak pernah sendiri ditemani bintang, semoga Allah menjadikan kami saling menerangi di setiap malam.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T09:00:00+07:00",
  place: "Gedung Serbaguna Masjid Raya Bintaro",
  address: "Jl. Bintaro Utama Sektor 3A, Pondok Aren, Tangerang Selatan",
  stories: [
    { date: "2024", title: "Kajian Malam Jumat", body: "Kami sama-sama menjadi panitia kajian remaja masjid. Pertemuan singkat di sela persiapan, tanpa banyak kata." },
    { date: "2026", title: "Ta'aruf", body: "Lewat perantara ustadzah, kami bertukar biodata dan istikharah. Keluarga bertemu dan saling merasa cocok." },
    { date: "2027", title: "Menuju Akad", body: "Di bawah langit yang sama, kami bersiap menyempurnakan separuh agama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Raya Bintaro Jaya", address: "Jl. Bintaro Utama Sektor 3A, Pondok Aren, Tangerang Selatan" },
    { name: "Walimatul 'Ursy", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Gedung Serbaguna Masjid Raya Bintaro", address: "Jl. Bintaro Utama Sektor 3A, Pondok Aren, Tangerang Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7209 5531 18", account_name: "Nabila Qonita Azzahra" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1270 0098 7654 3", account_name: "Muhammad Faris Al-Hakim" },
  ],
  guestName: "Ibu Hj. Fatimah & Keluarga",
  guestTable: "Meja Bintang 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Diiringi nasyid" },
      { time: "11.30", title: "Tausiyah pernikahan", note: "Ustadz Hanif Rasyidi" },
      { time: "12.15", title: "Ramah tamah", note: "Tamu putra & putri terpisah" },
    ] },
    dressCode: { note: "Busana muslim bernuansa pastel: lavender, biru periwinkle, atau krem.", colors: ["#c4b2e2", "#8f9bd8", "#f1d3df", "#fff4d8"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syamsul Bahri", "Kel. Besar Drs. Abdul Latif"] },
  },
});
