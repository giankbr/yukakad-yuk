import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Shafira", groom: "Daffa",
    brideFull: "Shafira Azzahra Putri, S.Psi.", groomFull: "Muhammad Daffa Alfarizi, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak H. Ridwan Firdaus & Ibu Hj. Siti Maryam", groomParents: "Putra kedua dari\nBapak Ir. H. Ahmad Zulfikar & Ibu Hj. Laila Fitriani",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seribu keping kaca kecil, satu cahaya yang sama. Semoga rumah kami kelak memantulkan kebaikan ke setiap sudutnya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-19T08:00:00+07:00",
  place: "The Trans Luxury Hotel Bandung",
  address: "Jl. Gatot Subroto No. 289, Cibangkong, Bandung",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Kajian Sabtu Pagi", body: "Kami duduk di barisan yang berseberangan pada sebuah kajian di Masjid Salman. Daffa yang mengembalikan buku catatan Shafira yang tertinggal." },
    { date: "2025", title: "Ta'aruf", body: "Lewat perantara guru mengaji, kami berkenalan dengan cara yang baik, saling bertanya tentang tujuan hidup dan rumah yang ingin dibangun." },
    { date: "2027", title: "Akad Nikah", body: "Dengan rida Allah dan restu kedua keluarga, kami mengikat janji suci di Bandung." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Salman ITB", address: "Jl. Ganesa No. 7, Lb. Siliwangi, Coblong, Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "The Trans Luxury Hotel Bandung", address: "Jl. Gatot Subroto No. 289, Cibangkong, Bandung" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/a31.webp", "/themes/img/a30.webp", "/themes/img/a137.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7154 2290 61", account_name: "Shafira Azzahra Putri" },
    { id: "demo-bjb", type: "bank", bank_name: "BJB", account_number: "0098 1276 5430 0", account_name: "Muhammad Daffa Alfarizi" },
  ],
  guestName: "Bapak H. Lukman Hakim & Keluarga",
  guestTable: "Meja Firuzeh 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu", note: "Diiringi nasyid dan marawis" },
      { time: "11.30", title: "Kirab pengantin" },
      { time: "12.00", title: "Doa & tausiyah singkat" },
      { time: "12.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim formal. Nuansa hijau toska, perak, dan rose gold dipersilakan.", colors: ["#0d3a3f", "#9db9b8", "#d49c84", "#eef2ef"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ridwan Firdaus", "Kel. Besar Ir. H. Ahmad Zulfikar"] },
    faq: { items: [
      { q: "Apakah tersedia tempat salat?", a: "Musala tersedia di lantai ballroom, lengkap dengan perlengkapan salat." },
      { q: "Di mana parkir tamu?", a: "Parkir tersedia di basement hotel dan area Trans Studio Mall." },
    ] },
  },
});
