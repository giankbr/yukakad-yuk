import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Yusuf",
    brideFull: "Salma Nabila Assegaf, Lc.", groomFull: "Yusuf Al Hakim, Lc., M.A.",
    brideParents: "Putri pertama dari\nBapak H. Hasan Assegaf & Ibu Hj. Fatimah Alaydrus", groomParents: "Putra ketiga dari\nBapak Dr. H. Mahmud Hakim & Ibu Hj. Aminah",
    note: "Semoga rumah tangga kami menjadi pelita: hangat di dalam, menerangi yang di sekitarnya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T10:00:00+07:00",
  place: "Aula Buya Hamka, Kompleks Masjid Agung Al-Azhar",
  address: "Jl. Sisingamangaraja, Selong, Kebayoran Baru, Jakarta Selatan",
  stories: [
    { date: "2019", title: "Ramadan di Kairo", body: "Dua mahasiswa Indonesia di Al-Azhar, bertemu di pengajian pelajar saat lentera fanous menghiasi lorong Sayyidah Zainab." },
    { date: "2022", title: "Pulang ke Tanah Air", body: "Kami lulus dan pulang membawa ilmu, sebuah fanous kecil, dan niat baik yang kami jaga dalam doa." },
    { date: "2026", title: "Khitbah", body: "Yusuf datang bersama keluarga ke rumah Salma, disambut teh hangat dan restu kedua orang tua." },
    { date: "2027", title: "Akad Nikah", body: "Insyaallah kami menyempurnakan separuh agama di masjid yang namanya mengingatkan kami pada Kairo." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja, Selong, Kebayoran Baru, Jakarta Selatan" },
    { name: "Walimah", date: "2027-10-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Buya Hamka", address: "Kompleks Masjid Agung Al-Azhar, Jl. Sisingamangaraja, Kebayoran Baru, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2288 31", account_name: "Salma Nabila Assegaf" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3310 0045 72", account_name: "Yusuf Al Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Kyai Maja No. 21, Kramat Pela, Kebayoran Baru, Jakarta Selatan 12130" },
  ],
  guestName: "Ustadz Fadlan Bahasuan & Keluarga",
  guestTable: "Meja Khalili 2",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Kedatangan mempelai", note: "Diiringi hadrah" },
      { time: "11.20", title: "Tausiyah walimah", note: "Oleh KH. Abdurrahman Faqih" },
      { time: "11.50", title: "Doa & ramah tamah", note: "Hidangan khas Timur Tengah" },
    ] },
    dressCode: { note: "Busana muslim rapi. Nuansa permata dipersilakan: merah delima, zamrud, kobalt, dan kuning tembaga.", colors: ["#d6283f", "#17a06c", "#2f5fdc", "#c99a52"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Hasan Assegaf", "Kel. Besar Dr. H. Mahmud Hakim"] },
  },
});
