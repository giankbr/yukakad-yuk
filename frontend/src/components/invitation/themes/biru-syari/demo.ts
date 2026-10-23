import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Syifa", groom: "Fadhil",
    brideFull: "Syifa Nur Rahmah, S.Farm.", groomFull: "Muhammad Fadhil Akbar, S.Kom.",
    brideParents: "Putri kedua dari\nBapak H. Dadang Suherman & Ibu Hj. Euis Kurniasih", groomParents: "Putra sulung dari\nBapak Ir. Ahmad Zaenuri & Ibu Siti Fatimah",
    note: "Semoga Allah menyatukan kami dalam kebaikan, dan menjadikan rumah kami tempat yang tenang untuk kembali.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung",
  stories: [
    { date: "2024", title: "Satu Kajian", body: "Kami sama-sama menjadi panitia kajian pekanan di masjid kampus, bertemu lewat rapat dan daftar hadir yang selalu Syifa rapikan." },
    { date: "2026", title: "Ta'aruf", body: "Melalui guru ngaji Fadhil, biodata kami dipertukarkan. Setelah istikharah, keluarga Fadhil bersilaturahmi ke rumah di Antapani." },
    { date: "Februari 2027", title: "Khitbah", body: "Lamaran sederhana di ruang tamu, dengan teh hangat, kue balok, dan doa dari kedua keluarga." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Graha Manggala Siliwangi", address: "Jl. Aceh No. 66, Merdeka, Sumur Bandung, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7204 1186 53", account_name: "Syifa Nur Rahmah" },
    { id: "demo-bjbs", type: "bank", bank_name: "bjb syariah", account_number: "5130 2004 7781", account_name: "Muhammad Fadhil Akbar" },
    { id: "demo-kado", type: "address", address: "Jl. Purwakarta No. 41, Antapani Kidul, Kota Bandung 40291", account_name: "Keluarga H. Dadang Suherman" },
  ],
  guestName: "Ibu Hj. Nenden Rohayati & Keluarga",
  guestTable: "Meja Biru 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Khusus keluarga inti dan wali" },
      { time: "11.00", title: "Penyambutan tamu" },
      { time: "11.30", title: "Tausiyah pernikahan" },
      { time: "12.15", title: "Ramah tamah & doa penutup" },
    ] },
    dressCode: { note: "Busana muslim rapi. Biru muda, putih, dan abu dipersilakan.", colors: ["#7896b6", "#a9c0d6", "#f3f1ea", "#9aa3ab"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dadang Suherman", "Kel. Besar Ir. Ahmad Zaenuri"] },
  },
});
