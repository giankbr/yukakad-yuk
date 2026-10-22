import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Yosi", groom: "Frans",
    brideFull: "Yosefina Maria Parera, S.Kep.", groomFull: "Fransiskus Xaverius Da Silva, S.T.",
    brideParents: "Putri sulung dari\nBapak Aloysius Parera & Ibu Theresia Nona Ema", groomParents: "Putra kedua dari\nBapak Mikael Da Silva & Ibu Margaretha Lusia",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti tiga danau Kelimutu yang berubah warna namun tetap di satu gunung, kami ingin tumbuh bersama dalam setiap musim.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T09:00:00+08:00",
  place: "Gereja Katedral St. Yosef Maumere",
  address: "Jl. Ahmad Yani, Kota Uneng, Alok, Kabupaten Sikka, Nusa Tenggara Timur",
  stories: [
    { date: "2019", title: "Pagi di Kelimutu", body: "Kami bertemu di puncak Kelimutu saat menunggu matahari terbit. Kabut tebal, tapi obrolan kami hangat." },
    { date: "2024", title: "Belis & Restu", body: "Kedua keluarga duduk bersama, bertukar tenun ikat Sikka sebagai tanda ikatan dan hormat." },
    { date: "2027", title: "Sakramen Perkawinan", body: "Di hadapan Tuhan dan umat, kami saling berjanji setia dalam suka dan duka." },
  ],
  events: [
    { name: "Sakramen Perkawinan", date: "2027-09-25T09:00:00+08:00", time: "09.00 – 11.00 WITA", venue: "Gereja Katedral St. Yosef Maumere", address: "Jl. Ahmad Yani, Kota Uneng, Alok, Kabupaten Sikka, NTT" },
    { name: "Resepsi", date: "2027-09-25T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Aula Paroki St. Yosef", address: "Jl. Ahmad Yani, Kota Uneng, Alok, Kabupaten Sikka, NTT" },
  ],
  gallery: ["/themes/img/r102.webp", "/themes/img/r107.webp", "/themes/img/r106.webp", "/themes/img/r84.webp", "/themes/img/r85.webp"],
  gifts: [
    { id: "demo-bntt", type: "bank", bank_name: "Bank NTT", account_number: "019 01 02 334455 6", account_name: "Yosefina Maria Parera" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0412 01 556677 50 1", account_name: "Fransiskus Xaverius Da Silva" },
  ],
  guestName: "Bapak Yohanes Fernandez & Keluarga",
  guestTable: "Meja Tiwu 2",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu.", source: "1 Korintus 13:4, 7" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Diiringi musik gong waning" },
      { time: "17.30", title: "Doa & sambutan keluarga" },
      { time: "18.30", title: "Makan bersama" },
      { time: "19.30", title: "Dansa & hiburan" },
    ] },
    dressCode: { note: "Busana resmi atau tenun ikat Sikka. Nila tua, karat, dan krem dipersilakan.", colors: ["#2b2130", "#a24a27", "#e3d3b0", "#2fb5a6"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-25T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Aloysius Parera", "Kel. Besar Mikael Da Silva"] },
  },
});
