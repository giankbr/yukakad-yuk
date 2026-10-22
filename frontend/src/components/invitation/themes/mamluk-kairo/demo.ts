import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Hanif",
    brideFull: "Aisyah Nur Hidayah, Lc.", groomFull: "Hanif Abdurrasyid, Lc., M.A.",
    brideParents: "Putri kedua dari\nBapak K.H. Mahfudz Siddiq & Ibu Hj. Fatimah Zahra", groomParents: "Putra pertama dari\nBapak H. Ridwan Hakim & Ibu Hj. Maryam Ulfa",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Bertemu di lorong-lorong batu Kairo yang berlapis merah dan putih, kami belajar bahwa yang kokoh dibangun selapis demi selapis.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-12-04T09:00:00+07:00",
  place: "Gedung Serbaguna Al-Azhar",
  address: "Jl. Sisingamangaraja, Kebayoran Baru, Jakarta Selatan",
  stories: [
    { date: "2019", title: "Talaqqi di Al-Azhar", body: "Kami sama-sama menuntut ilmu di Kairo dan pertama kali bertemu di sebuah majelis kajian mahasiswa Indonesia di Hay el-Asher." },
    { date: "2024", title: "Pulang ke Tanah Air", body: "Setelah lulus, kami kembali mengajar di pesantren masing-masing; Hanif datang bersama keluarga untuk khitbah di Bogor." },
    { date: "2027", title: "Akad", body: "Bismillah, kami memulai bangunan kecil kami: rumah yang tenang, selapis demi selapis." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-12-04T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja, Kebayoran Baru, Jakarta Selatan" },
    { name: "Walimatul 'Ursy", date: "2027-12-04T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Al-Azhar", address: "Jl. Sisingamangaraja, Kebayoran Baru, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a139.webp", "/themes/img/r63.webp", "/themes/img/r3.webp", "/themes/img/r4.webp", "/themes/img/r0.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7166 0928 33", account_name: "Aisyah Nur Hidayah" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3010 0482 71", account_name: "Hanif Abdurrasyid" },
    { id: "demo-kado", type: "address", address: "Jl. Pahlawan No. 17, Bondongan, Bogor Selatan, Kota Bogor 16131" },
  ],
  guestName: "Bapak Dr. H. Salman Farisi & Keluarga",
  guestTable: "Meja Qalawun 4",
  extras: {
    quote: { text: "Mereka adalah pakaian bagimu, dan kamu adalah pakaian bagi mereka.", source: "QS. Al-Baqarah: 187" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Lantunan shalawat & gambus" },
      { time: "11.30", title: "Kedatangan kedua mempelai" },
      { time: "12.00", title: "Tausiyah pernikahan" },
      { time: "12.30", title: "Jamuan", note: "Nasi mandi, kofta & kunafa" },
    ] },
    dressCode: { note: "Busana muslim formal dalam warna batu pasir, merah bata, atau biru tua.", colors: ["#e9d6b0", "#a9583a", "#3b302c", "#2e5d8a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar K.H. Mahfudz Siddiq", "Kel. Besar H. Ridwan Hakim", "Keluarga Alumni Al-Azhar Mesir"] },
  },
});
