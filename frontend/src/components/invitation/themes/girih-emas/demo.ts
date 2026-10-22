import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laila", groom: "Haidar",
    brideFull: "Laila Syahidah Rahmani, M.Ars.", groomFull: "Haidar Ali Firdaus, S.T.",
    brideParents: "Putri kedua dari\nBapak Ir. H. Rahmat Hidayatullah & Ibu Hj. Zahra Fitriani", groomParents: "Putra sulung dari\nBapak Dr. H. Muhammad Arifin & Ibu Hj. Nurul Hikmah",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti garis-garis girih yang tak pernah terputus, semoga ikatan ini terus bersambung dalam keberkahan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-11-13T08:00:00+07:00",
  place: "Masjid Cut Meutia",
  address: "Jl. Taman Cut Mutiah No. 1, Gondangdia, Menteng, Jakarta Pusat",
  stories: [
    { date: "2021", title: "Satu Studio Gambar", body: "Kami bertemu di kelas sejarah arsitektur Islam: ia menggambar ulang ubin Isfahan, aku sibuk menghitung sudutnya." },
    { date: "2024", title: "Proyek Restorasi", body: "Bertahun kemudian kami satu tim merestorasi mihrab masjid tua di Banten. Dari situ obrolan kami tak pernah selesai." },
    { date: "Juni 2027", title: "Khitbah", body: "Keluarga Haidar datang ke Rawamangun dengan doa, kurma, dan sebuah sketsa girih berbingkai emas." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-11-13T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Cut Meutia", address: "Jl. Taman Cut Mutiah No. 1, Gondangdia, Menteng, Jakarta Pusat" },
    { name: "Resepsi Malam", date: "2027-11-13T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Gedung Sasana Kriya", address: "Taman Mini Indonesia Indah, Jl. Raya Taman Mini, Cipayung, Jakarta Timur" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/r6.webp", "/themes/img/r1.webp", "/themes/img/r3.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7203 1186 4420", account_name: "Laila Syahidah Rahmani" },
    { id: "demo-bca", type: "bank", bank_name: "BCA Syariah", account_number: "0218 5530 77", account_name: "Haidar Ali Firdaus" },
  ],
  guestName: "Bapak H. Fadli Ramadhan & Keluarga",
  guestTable: "Meja Isfahan 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah & doa bersama" },
      { time: "19.00", title: "Resepsi dibuka", note: "Jamuan malam" },
      { time: "20.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim formal bernuansa malam: biru tua, gading, dan aksen emas.", colors: ["#0b1633", "#16285a", "#caa553", "#efe3c4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-11-13T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Rahmat Hidayatullah", "Kel. Besar Dr. H. Muhammad Arifin", "Ikatan Alumni Arsitektur UI"] },
    faq: { items: [
      { q: "Apakah tersedia tempat salat?", a: "Ya, musala tersedia di sayap barat Sasana Kriya untuk salat Isya." },
      { q: "Di mana parkir untuk resepsi?", a: "Parkir tamu tersedia di area depan Sasana Kriya, masuk melalui Gerbang Utama TMII." },
    ] },
  },
});
