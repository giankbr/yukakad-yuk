import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Fadhil",
    brideFull: "Zahra Khairunnisa, S.Farm.", groomFull: "Muhammad Fadhil Abdurrahman, Lc.",
    brideParents: "Putri pertama dari\nBapak H. Ahmad Syarifuddin & Ibu Hj. Nurlaela", groomParents: "Putra ketiga dari\nBapak K.H. Abdul Hamid & Ibu Hj. Siti Maryam",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Semoga Allah menghimpun kami dalam kebaikan, dan menjadikan rumah kami tempat bersujud yang teduh.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-02-20T08:00:00+07:00",
  place: "Balai Kartini",
  address: "Jl. Gatot Subroto Kav. 37, Kuningan, Jakarta Selatan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2021", title: "Majelis Ilmu", body: "Kami pertama kali bertemu sebagai panitia kajian pekanan di sebuah masjid kampus di Depok." },
    { date: "2025", title: "Ta'aruf", body: "Atas perantara guru kami, proses ta'aruf berjalan dengan tenang bersama kedua keluarga." },
    { date: "2026", title: "Khitbah", body: "Fadhil datang bersama keluarga untuk mengkhitbah, disambut dengan doa dan haru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-02-20T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sunda Kelapa", address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat" },
    { name: "Walimatul 'Ursy", date: "2027-02-20T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Kartini", address: "Jl. Gatot Subroto Kav. 37, Kuningan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/r57.webp", "/themes/img/r58.webp", "/themes/img/r84.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2233 51", account_name: "Zahra Khairunnisa" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3010 0456 7788", account_name: "Muhammad Fadhil Abdurrahman" },
    { id: "demo-kado", type: "address", address: "Jl. Kenari II No. 8, Kenari, Senen, Jakarta Pusat 10430" },
  ],
  guestName: "Ustadz Hasan Basri & Keluarga",
  guestTable: "Meja 9",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "08.20", title: "Ijab kabul", note: "Keluarga inti & saksi" },
      { time: "08.45", title: "Khutbah nikah & doa" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
    ] },
    dressCode: { note: "Busana muslim yang santun. Nuansa merah anggur, emas, dan hijau tua.", colors: ["#5c1124", "#c9a14a", "#1d4a44", "#f4ead8"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-02-20T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar K.H. Abdul Hamid"] },
  },
});
