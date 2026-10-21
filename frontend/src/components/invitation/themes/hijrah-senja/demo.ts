import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Faris",
    brideFull: "Salma Khairunnisa, S.Psi.", groomFull: "Faris Abdurrahman, S.E.",
    brideParents: "Putri sulung dari\nBapak H. Ridwan Syarifuddin & Ibu Hj. Laila Fitri", groomParents: "Putra ketiga dari\nBapak H. Anwar Syahputra & Ibu Hj. Rosmawati",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti kafilah yang berjalan pulang saat senja, kami ingin menempuh perjalanan ini bersama, menuju rida-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-18T08:00:00+07:00",
  place: "Masjid Al-Irsyad Satya",
  address: "Kota Baru Parahyangan, Padalarang, Kabupaten Bandung Barat",
  stories: [
    { date: "2023", title: "Satu Majelis", body: "Kami sama-sama belajar di kajian pekanan yang sama, tanpa saling mengenal lebih dari sekadar nama." },
    { date: "2025", title: "Ta'aruf", body: "Lewat perantara ustazah, kami bertukar biodata dan bertemu dengan didampingi keluarga." },
    { date: "2026", title: "Lamaran", body: "Faris datang meminang di rumah keluarga Salma, ba'da Magrib, saat langit Bandung berwarna jingga." },
    { date: "2027", title: "Akad", body: "Insyaallah kami memulai perjalanan baru dalam ikatan yang diridai Allah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Irsyad Satya", address: "Kota Baru Parahyangan, Padalarang, Kabupaten Bandung Barat" },
    { name: "Walimatul 'Ursy", date: "2027-09-18T16:00:00+07:00", time: "16.00 – 19.00 WIB", venue: "Taman Senja Parahyangan", address: "Jl. Parahyangan Raya No. 8, Kota Baru Parahyangan, Bandung Barat" },
  ],
  gallery: ["/themes/img/a33.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a21.webp", "/themes/img/a111.webp", "/themes/img/a116.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7311 2024 8890", account_name: "Salma Khairunnisa" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2830 4455 17", account_name: "Faris Abdurrahman" },
  ],
  guestName: "Bapak H. Usman Effendi & Keluarga",
  guestTable: "Meja Kafilah 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu", note: "Teh hangat & kurma" },
      { time: "16.30", title: "Tausiyah walimah" },
      { time: "17.40", title: "Jeda salat Magrib", note: "Musala di sisi taman" },
      { time: "18.15", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa senja: plum, terakota, pasir, dan emas kuningan.", colors: ["#5a2f4f", "#b0614d", "#e8c79a", "#b9873a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ridwan Syarifuddin", "Kel. Besar H. Anwar Syahputra"] },
  },
});
