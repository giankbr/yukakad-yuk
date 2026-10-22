import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Khadijah", groom: "Hamzah",
    brideFull: "Khadijah Nur Rahmania, S.Pd.", groomFull: "Hamzah Abdurrahman Basyaib, S.E.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Fauzan Baraqbah & Ibu Hj. Nurlaila Assegaf",
    groomParents: "Putra sulung dari\nBapak H. Umar Basyaib & Ibu Hj. Fatimah Alhabsyi",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti cahaya yang menembus kisi-kisi kayu, semoga kasih sayang kami selalu menemukan jalannya dengan lembut.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-07-10T09:00:00+07:00",
  place: "Masjid Ampel",
  address: "Jl. Ampel Masjid No. 53, Ampel, Semampir, Surabaya",
  stories: [
    { date: "2019", title: "Kampung Ampel", body: "Kami tumbuh di gang yang sama, di antara toko kurma, minyak wangi, dan jendela-jendela kayu berkisi." },
    { date: "2025", title: "Ta'aruf", body: "Lewat perantara ustadzah keluarga, kami bertukar biodata dan bertemu dengan didampingi orang tua." },
    { date: "April 2027", title: "Khitbah", body: "Keluarga Hamzah datang meminang, disambut teh rempah dan doa para sesepuh." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Ampel", address: "Jl. Ampel Masjid No. 53, Ampel, Semampir, Surabaya" },
    { name: "Walimah", date: "2027-07-10T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Gedung Al-Irsyad Surabaya", address: "Jl. K.H. Mas Mansyur No. 166, Nyamplungan, Pabean Cantian, Surabaya" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a49.webp", "/themes/img/a43.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 8834 51", account_name: "Khadijah Nur Rahmania" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "081233418890", account_name: "Hamzah Abdurrahman" },
  ],
  guestName: "Bapak H. Salim Bawazier & Keluarga",
  guestTable: "Meja Gaharu 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "09.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Doa & tausiyah" },
      { time: "18.30", title: "Walimah dibuka", note: "Jamuan nasi kebuli" },
      { time: "20.00", title: "Hadrah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim santun. Nuansa cokelat kayu, madu, dan krem dipersilakan.", colors: ["#7a4a26", "#d29a4e", "#f4ead8", "#3b2414"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-10T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Fauzan Baraqbah", "Kel. Besar H. Umar Basyaib"] },
  },
});
