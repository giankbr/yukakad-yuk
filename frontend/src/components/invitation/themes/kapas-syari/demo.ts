import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hanifa", groom: "Fadhil",
    brideFull: "Hanifa Nur Azizah, S.Pd.", groomFull: "Muhammad Fadhil Ramadhan, S.P.",
    brideParents: "Putri pertama dari\nBapak H. Sulaiman Effendi & Ibu Hj. Siti Maesaroh",
    groomParents: "Putra ketiga dari\nBapak Abdul Rasyid & Ibu Nurhayati",
    note: "Sesederhana kapas yang merekah di ujung tangkai kering: putih, ringan, dan cukup.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-14T08:00:00+07:00",
  place: "Masjid Al-Ikhlas Jatinangor",
  address: "Jl. Raya Jatinangor No. 88, Cibeusi, Jatinangor, Kabupaten Sumedang",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2023", title: "Satu Halaqah", body: "Kami sama-sama mengajar TPA di masjid kampus, di ruang yang berbeda, dengan salam yang sesekali bertemu di serambi." },
    { date: "2026", title: "Ta'aruf", body: "Lewat perantara guru mengaji, kami bertukar biodata, lalu bertemu dengan didampingi keluarga." },
    { date: "Februari 2027", title: "Khitbah", body: "Keluarga Fadhil datang ke Sumedang dengan niat baik, dan dengan izin Allah lamaran diterima." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Ikhlas Jatinangor", address: "Jl. Raya Jatinangor No. 88, Cibeusi, Jatinangor, Kabupaten Sumedang" },
    { name: "Walimah", date: "2027-08-14T10:30:00+07:00", time: "10.30 – 13.00 WIB", venue: "Kediaman Keluarga H. Sulaiman", address: "Jl. Kolonel Ahmad Syam Gg. Kenanga No. 7, Hegarmanah, Jatinangor, Sumedang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7181 2046 33", account_name: "Hanifa Nur Azizah" },
    { id: "demo-address", type: "address", address: "Jl. Kolonel Ahmad Syam Gg. Kenanga No. 7, Hegarmanah, Jatinangor, Sumedang 45363", account_name: "Keluarga H. Sulaiman Effendi" },
  ],
  guestName: "Ibu Hj. Rukmini & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "10.30", title: "Walimah sederhana", note: "Tamu putra & putri di ruang terpisah" },
      { time: "12.30", title: "Doa bersama & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Warna krem, putih gading, dan cokelat muda dipersilakan.", colors: ["#f3ecdf", "#d9c7a8", "#a07a55", "#6e5440"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Sulaiman Effendi", "Kel. Besar Abdul Rasyid"] },
  },
});
