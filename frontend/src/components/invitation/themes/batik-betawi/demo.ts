import { makeDemo } from "../demo-base";

// Betawi pesisir: akad nikah di masjid, lalu palang pintu (rombongan abang dengan silat & pantun) dan resepsi dekat
// pelabuhan Sunda Kelapa.
export const demo = makeDemo({
  couple: {
    bride: "Nurul", groom: "Fadli",
    brideFull: "Siti Nurul Hasanah, S.Pd.", groomFull: "Muhammad Fadli Ramadhan, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Sa'ari Usman & Ibu Hj. Mariam", groomParents: "Putra kedua dari\nBapak H. Rojali Saidi & Ibu Hj. Rohaya",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Kayak kain batik pesisir: banyak warnanye, tapi jadi satu lembar yang indah. Doain kite ye.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T08:00:00+07:00",
  place: "Gedung Serbaguna Sunda Kelapa",
  address: "Jl. Pakin No. 7, Penjaringan, Jakarta Utara",
  stories: [
    { date: "2020", title: "Ketemu di Kota Tua", body: "Sama-sama jadi relawan festival budaya Betawi. Nurul jaga stan kerak telor, Fadli jaga panggung gambang kromong." },
    { date: "2024", title: "Ngelamar", body: "Dengan rombongan keluarga dan seserahan roti buaya, Fadli datang meminang ke rumah Babe Sa'ari." },
    { date: "2027", title: "Ijab Kabul", body: "Insyaallah kami menyempurnakan separuh agama, disaksikan keluarga besar dan sahabat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jami' Al-Makmur", address: "Jl. Raden Saleh Raya No. 30, Cikini, Menteng, Jakarta Pusat" },
    { name: "Palang Pintu & Resepsi", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Sunda Kelapa", address: "Jl. Pakin No. 7, Penjaringan, Jakarta Utara" },
  ],
  gallery: ["/themes/img/a100.webp", "/themes/img/r70.webp", "/themes/img/a124.webp", "/themes/img/r38.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank DKI", account_number: "101 2345 678", account_name: "Siti Nurul Hasanah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7120 8899 31", account_name: "Muhammad Fadli Ramadhan" },
    { id: "demo-kado", type: "address", address: "Jl. Kampung Bandan Gg. III No. 21, Ancol, Pademangan, Jakarta Utara 14430" },
  ],
  guestName: "Bapak H. Muhidin & Keluarga",
  guestTable: "Meja Kembang 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Palang pintu", note: "Rombongan abang datang dengan silat, pantun & sike" },
      { time: "11.30", title: "Kirab penganten diiringi tanjidor" },
      { time: "12.00", title: "Ramah tamah & hidangan Betawi", note: "Soto Betawi, gabus pucung, bir pletok" },
      { time: "13.15", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Batik pesisir atau baju sadariah & kebaya encim. Merah, hijau, dan kuning dipersilakan.", colors: ["#c4252c", "#1f7a3e", "#f2b62a", "#f7ead0"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-12T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Sa'ari Usman (Kampung Bandan)", "Kel. Besar H. Rojali Saidi (Marunda)"] },
  },
});
