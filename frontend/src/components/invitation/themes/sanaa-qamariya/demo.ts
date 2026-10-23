import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nabila", groom: "Faris",
    brideFull: "Nabila Azzahra, S.Ars.", groomFull: "Muhammad Faris Alamsyah, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Zaki & Ibu Hj. Nurul Hikmah", groomParents: "Putra pertama dari\nBapak Drs. Hasan Alamsyah & Ibu Siti Maryam",
    note: "Seperti cahaya senja yang menembus kaca qamariya, semoga cinta kami selalu memberi warna dan teduh bagi orang di sekitar.",
  },
  eventLabel: "Walimatul 'Urs",
  date: "2027-10-09T08:00:00+07:00",
  place: "Aula Barat ITB",
  address: "Jl. Ganesa No. 10, Lb. Siliwangi, Kec. Coblong, Kota Bandung",
  stories: [
    { date: "2020", title: "Studio Arsitektur", body: "Kami satu kelompok tugas sejarah arsitektur, menggambar ulang rumah-rumah menara kota tua Sana'a sampai larut malam." },
    { date: "2024", title: "Taaruf", body: "Bertahun-tahun berteman, Faris akhirnya datang ke rumah bersama keluarganya dengan niat yang baik." },
    { date: "2027", title: "Menuju Akad", body: "Dengan restu kedua orang tua, kami memohon doa agar rumah tangga kami penuh sakinah, mawaddah, dan rahmah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung" },
    { name: "Walimah", date: "2027-10-09T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Barat ITB", address: "Jl. Ganesa No. 10, Lb. Siliwangi, Kec. Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a118.webp", "/themes/img/a33.webp", "/themes/img/a26.webp", "/themes/img/a110.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7209 1027 31", account_name: "Nabila Azzahra" },
    { id: "demo-kado", type: "address", address: "Jl. Cisitu Lama No. 18, Dago, Kec. Coblong, Kota Bandung 40135" },
  ],
  guestName: "Bapak H. Ridwan Kamal & Keluarga",
  guestTable: "7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka" },
      { time: "12.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim rapi dengan nuansa senja: bata, krem, dan biru malam.", colors: ["#7c4e36", "#f4ede1", "#2c2f62", "#e5a35a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Zaki", "Kel. Besar Drs. Hasan Alamsyah"] },
  },
});
