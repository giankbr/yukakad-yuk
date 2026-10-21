import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Faris",
    brideFull: "Nadhira Az-Zahra Hanifah, S.Ars.", groomFull: "Faris Alfarizi Hakim, S.T.",
    brideParents: "Putri pertama dari\nBapak H. Abdul Rahman Hakim & Ibu Hj. Siti Mardiyah",
    groomParents: "Putra kedua dari\nBapak Ir. H. Taufik Hidayat & Ibu Dra. Hj. Lailatul Fitriyah",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti kepingan zellige yang disusun satu per satu, semoga Allah menyusun hari-hari kami menjadi indah dan utuh.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Raya Bintaro Jaya",
  address: "Jl. Bintaro Utama 3A, Pondok Karya, Pondok Aren, Tangerang Selatan",
  stories: [
    { date: "2021", title: "Satu Studio", body: "Kami bertemu di studio arsitektur, sama-sama terpikat pada pola geometri masjid-masjid tua." },
    { date: "2024", title: "Ta'aruf", body: "Dengan perantara guru ngaji keluarga, kami berkenalan lebih dekat dan saling menimbang dengan istikharah." },
    { date: "Februari 2027", title: "Khitbah", body: "Keluarga Faris datang bersilaturahmi, meminang dengan penuh kehangatan dan doa." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bintaro Jaya", address: "Jl. Bintaro Utama 3A, Pondok Karya, Pondok Aren, Tangerang Selatan" },
    { name: "Walimah", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Taman Andalus", address: "Jl. Kebayoran Lama No. 34, Grogol Utara, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a18.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Nadhira Az-Zahra Hanifah" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "081377654321", account_name: "Faris Alfarizi Hakim" },
  ],
  guestName: "Bapak H. Ridwan Syamsudin & Keluarga",
  guestTable: "Meja Zaitun 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Jamuan di taman" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim santun. Hijau zamrud, toska, dan putih gading dipersilakan.", colors: ["#1f6a4f", "#1d7c82", "#f1ece0", "#c99a3e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-15T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Rahman Hakim", "Kel. Besar Ir. H. Taufik Hidayat"] },
  },
});
