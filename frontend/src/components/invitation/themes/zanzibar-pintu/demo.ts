import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Faris",
    brideFull: "Salma Nur Azizah Alaydrus, S.Ars.", groomFull: "Faris Hamid Basyaiban, S.T.",
    brideParents: "Putri kedua dari\nBapak Husein Alaydrus & Ibu Fatimah Assegaf", groomParents: "Putra pertama dari\nBapak Hamid Basyaiban & Ibu Nur Aini Bahasuan",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti pintu kayu yang dibuka dengan salam, kami membuka rumah kami dengan doa dan restu Anda.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+08:00",
  place: "Gedung Pertemuan Sasana Bahari",
  address: "Jl. Pelabuhan No. 7, Kampung Arab, Ampenan, Kota Mataram, NTB",
  stories: [
    { date: "2021", title: "Bertemu di Pelabuhan Tua", body: "Salma sedang mengukur fasad rumah-rumah tua di Ampenan untuk penelitian arsitekturnya, Faris kebetulan memperbaiki daun pintu rumah neneknya." },
    { date: "2024", title: "Khitbah", body: "Setelah ta'aruf yang dijaga kedua keluarga, Faris datang bersama orang tuanya untuk mengkhitbah Salma." },
    { date: "2027", title: "Membuka Pintu Baru", body: "Dengan memohon ridha Allah, kami melangkah bersama menuju akad dan rumah tangga yang sakinah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+08:00", time: "08.00 – 10.00 WITA", venue: "Masjid Raya Al-Ijtihad Ampenan", address: "Jl. Saleh Sungkar, Ampenan Tengah, Kota Mataram, NTB" },
    { name: "Walimah", date: "2027-05-15T11:00:00+08:00", time: "11.00 – 14.00 WITA", venue: "Gedung Pertemuan Sasana Bahari", address: "Jl. Pelabuhan No. 7, Kampung Arab, Ampenan, Kota Mataram, NTB" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/r38.webp", "/themes/img/a26.webp", "/themes/img/r109.webp", "/themes/img/r11.webp", "/themes/img/a118.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7180 2214 55", account_name: "Salma Nur Azizah" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5530 1987 22", account_name: "Faris Hamid Basyaiban" },
    { id: "demo-kado", type: "address", address: "Jl. Pabean No. 18, Kampung Arab, Ampenan, Kota Mataram 83114" },
  ],
  guestName: "Bapak Habib Umar Alatas & Keluarga",
  guestTable: "Meja Pemba",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Hadrah & marawis" },
      { time: "11.30", title: "Tausiyah pernikahan" },
      { time: "12.00", title: "Jamuan", note: "Nasi kebuli, gulai kambing & teh susu" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim yang santun bernuansa putih kapur, toska laut, dan cokelat jati.", colors: ["#efe6d4", "#3fb2b4", "#5e3b23", "#caa451"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Alaydrus – Assegaf", "Kel. Besar Basyaiban – Bahasuan", "Jamaah Masjid Raya Al-Ijtihad"] },
  },
});
