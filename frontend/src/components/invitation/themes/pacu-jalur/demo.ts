import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nurul", groom: "Fadhil",
    brideFull: "Nurul Aini Syahfitri, S.Pd.", groomFull: "Muhammad Fadhil Ramadhan, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Zulkifli Datuk Bandaro & Ibu Hj. Rosnidar", groomParents: "Putra sulung dari\nBapak Syamsul Bahri & Ibu Nur Asiah",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a60.webp",
    note: "Sedayung sehaluan, seiring sejalan: kami memulai pelayaran baru di tepian Batang Kuantan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-28T09:00:00+07:00",
  place: "Gedung Taman Jalur",
  address: "Jl. Ahmad Yani, Pasar Taluk, Kec. Kuantan Tengah, Teluk Kuantan, Kuantan Singingi, Riau",
  stories: [
    { date: "2019", title: "Di Tepian Narosa", body: "Kami bertemu di tengah sorak penonton Pacu Jalur, sama-sama mendukung jalur dari kampung masing-masing." },
    { date: "2023", title: "Sedayung Sehaluan", body: "Bertahun-tahun saling mengenal, belajar mendayung seirama walau arus kadang deras." },
    { date: "2027", title: "Menuju Tepian", body: "Dengan restu kedua keluarga, kami bersiap mengikat janji di kampung halaman, Teluk Kuantan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-28T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Al-Mukhlisin", address: "Jl. Prof. M. Yamin, Pasar Taluk, Kec. Kuantan Tengah, Teluk Kuantan" },
    { name: "Resepsi", date: "2027-08-28T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung Taman Jalur", address: "Jl. Ahmad Yani, Pasar Taluk, Kec. Kuantan Tengah, Teluk Kuantan, Kuantan Singingi, Riau" },
  ],
  gallery: ["/themes/img/a61.webp", "/themes/img/a72.webp", "/themes/img/a60.webp", "/themes/img/a33.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-brk", type: "bank", bank_name: "BRK Syariah", account_number: "8120 4417 0293", account_name: "Nurul Aini Syahfitri" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7166 2045 18", account_name: "Muhammad Fadhil Ramadhan" },
    { id: "demo-kado", type: "address", address: "Jl. Perintis Kemerdekaan No. 27, Sungai Jering, Kuantan Tengah, Teluk Kuantan 29511" },
  ],
  guestName: "Bapak H. Datuk Rajo Mangkuto & Keluarga",
  guestTable: "Tepian 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Diiringi rebana dan silat pengantin" },
      { time: "11.30", title: "Bersanding di pelaminan" },
      { time: "12.30", title: "Makan bajamba bersama" },
    ] },
    dressCode: { note: "Baju kurung atau teluk belanga. Kuning, merah, dan hijau dipersilakan.", colors: ["#e9b52c", "#c0352a", "#2f7a4c", "#f6ead0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkifli Datuk Bandaro", "Kel. Besar Syamsul Bahri"] },
  },
});
