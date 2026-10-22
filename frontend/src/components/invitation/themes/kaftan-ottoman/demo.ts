import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hana", groom: "Emir",
    brideFull: "Hana Safiya Rahman, S.Psi.", groomFull: "Muhammad Emir Fadhillah, S.H.",
    brideParents: "Putri pertama dari\nBapak Ir. H. Arif Rahman & Ibu Hj. Nadia Kamila", groomParents: "Putra kedua dari\nBapak H. Fadhil Hasan & Ibu Hj. Laila Syarifah",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Semoga Allah menghimpun kami dalam kebaikan, seperti benang emas yang ditenun menjadi satu kain.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-02-20T09:00:00+07:00",
  place: "Balai Kartini",
  address: "Jl. Gatot Subroto Kav. 37, Kuningan Timur, Setiabudi, Jakarta Selatan",
  stories: [
    { date: "2018", title: "Kelas Sejarah Seni", body: "Kami duduk bersebelahan di kuliah umum tentang kain-kain Utsmani, dan sama-sama terpaku pada sehelai kaftan berbenang emas." },
    { date: "2024", title: "Khitbah", body: "Emir datang bersama keluarga untuk meminang. Doa dan restu menjadi benang pertama kain kami." },
    { date: "2027", title: "Akad", body: "Dengan rahmat Allah, kami menenun hari-hari baru sebagai suami dan istri." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-02-20T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja No. 1, Selong, Kebayoran Baru, Jakarta Selatan" },
    { name: "Walimatul 'Ursy", date: "2027-02-20T11:30:00+07:00", time: "11.30 – 14.30 WIB", venue: "Balai Kartini", address: "Jl. Gatot Subroto Kav. 37, Kuningan Timur, Setiabudi, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a118.webp", "/themes/img/r57.webp", "/themes/img/r58.webp", "/themes/img/a85.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7155 6677 88", account_name: "Hana Safiya Rahman" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5270 4412 09", account_name: "Muhammad Emir Fadhillah" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Timur Raya No. 18, Bangka, Mampang Prapatan, Jakarta Selatan 12730" },
  ],
  guestName: "Bapak H. Kamal Pasha & Keluarga",
  guestTable: "Meja Lale 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.30", title: "Penyambutan tamu", note: "Iringan gambus & marawis" },
      { time: "12.00", title: "Kedatangan kedua mempelai" },
      { time: "12.30", title: "Jamuan", note: "Nasi kebuli & kopi rempah" },
      { time: "13.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim formal. Merah marun, emas, dan krem dipersilakan.", colors: ["#8e1420", "#d7b35e", "#f3e6c8", "#5a0a12"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-02-20T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ir. H. Arif Rahman", "Kel. Besar H. Fadhil Hasan"] },
  },
});
