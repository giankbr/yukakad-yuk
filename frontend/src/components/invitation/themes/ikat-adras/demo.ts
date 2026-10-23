import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Fikri",
    brideFull: "Salma Khairunnisa, S.Ds.", groomFull: "Fikri Ramadhan Hakim, M.Sc.",
    brideParents: "Putri pertama dari\nBapak Dr. H. Ahmad Zulkarnain & Ibu Hj. Nurul Fadhilah", groomParents: "Putra kedua dari\nBapak H. Irwan Hakim & Ibu Siti Maryam",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Dua benang yang berbeda warna, diikat dan dicelup dalam doa yang sama, lalu ditenun menjadi satu kain.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T08:00:00+07:00",
  place: "Graha Sanusi Hardjadinata",
  address: "Jl. Dipati Ukur No. 35, Lebakgede, Coblong, Kota Bandung",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2021", title: "Pameran tekstil", body: "Salma meneliti kain ikat untuk tugas akhirnya, Fikri menjadi relawan pemandu pameran wastra di Bandung. Kami berdebat soal warna, lalu tak berhenti bertukar cerita." },
    { date: "2025", title: "Belajar dan menunggu", body: "Fikri menempuh studi di Tashkent. Dari sana ia mengirim foto pasar kain adras, dan Salma menyimpan setiap warnanya." },
    { date: "2027", title: "Khitbah", body: "Sepulang Fikri, keluarga kami bersilaturahmi. Dengan restu kedua orang tua, kami mantap menyempurnakan separuh agama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Salman ITB", address: "Jl. Ganesa No. 7, Lb. Siliwangi, Coblong, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-10-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Sanusi Hardjadinata", address: "Jl. Dipati Ukur No. 35, Lebakgede, Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/r6.webp", "/themes/img/r63.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Salma Khairunnisa" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 2233 4455", account_name: "Fikri Ramadhan Hakim" },
  ],
  guestName: "Ibu Dr. Hj. Laila Fitriani & Keluarga",
  guestTable: "Meja Atlas 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin", note: "Diiringi rebana" },
      { time: "11.30", title: "Doa dan tausiyah singkat" },
      { time: "12.00", title: "Ramah tamah dan santap siang" },
      { time: "13.00", title: "Foto bersama keluarga dan sahabat" },
    ] },
    dressCode: { note: "Busana muslim formal. Warna berani khas adras: magenta, kunyit, zamrud, dan nila.", colors: ["#c0185e", "#eba51e", "#0f7a52", "#23306e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Dr. H. Ahmad Zulkarnain", "Kel. Besar H. Irwan Hakim"] },
  },
});
