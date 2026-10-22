import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Fitri", groom: "Rizal",
    brideFull: "Fitriani Nur Marsaoly, S.Farm.", groomFull: "Ahmad Rizal Hi. Taher, S.T.",
    brideParents: "Putri sulung dari\nBapak H. Jafar Marsaoly & Ibu Hj. Nurlela Abbas", groomParents: "Putra ketiga dari\nBapak Hi. Hamid Taher & Ibu Salma Duwila",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti pala dan cengkih yang tumbuh di lereng yang sama, semoga kami saling menjaga dan saling mengharumkan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T09:00:00+09:00",
  place: "Masjid Sultan Ternate",
  address: "Jl. Sultan Babullah, Soa-Sio, Ternate Utara, Kota Ternate, Maluku Utara",
  stories: [
    { date: "2021", title: "Pagi di Benteng Oranje", body: "Kami bertemu di sebuah kegiatan bersih pantai. Fitri membawa termos teh rempah, Rizal yang paling sering menambah gelas." },
    { date: "2025", title: "Antar Tanda", body: "Keluarga Rizal datang membawa tanda ikatan. Di kaki Gamalama, dua keluarga sepakat menyatukan kami." },
    { date: "2027", title: "Akad Nikah", body: "Dengan memohon rida Allah, kami melangkah ke ikatan yang suci di Masjid Sultan Ternate." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T09:00:00+09:00", time: "09.00 – 10.30 WIT", venue: "Masjid Sultan Ternate", address: "Jl. Sultan Babullah, Soa-Sio, Ternate Utara, Kota Ternate" },
    { name: "Walimatul 'Ursy", date: "2027-10-09T19:00:00+09:00", time: "19.00 – 22.00 WIT", venue: "Gedung Serba Guna Jati", address: "Jl. Sultan Khairun No. 21, Kalumpang, Ternate Tengah, Kota Ternate" },
  ],
  gallery: ["/themes/img/a33.webp", "/themes/img/r84.webp", "/themes/img/r102.webp", "/themes/img/r5.webp", "/themes/img/r89.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 5522 81", account_name: "Fitriani Nur Marsaoly" },
    { id: "demo-bmalut", type: "bank", bank_name: "Bank Malut", account_number: "002 01 11 07731 0", account_name: "Ahmad Rizal Hi. Taher" },
  ],
  guestName: "Bapak H. Abdurrahman Sangaji & Keluarga",
  guestTable: "Meja Pala 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.00", title: "Penyambutan tamu", note: "Diiringi tifa dan lagu daerah Ternate" },
      { time: "19.30", title: "Doa & sambutan keluarga" },
      { time: "20.00", title: "Ramah tamah", note: "Gohu ikan dan kue rempah" },
      { time: "21.00", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim resmi. Biru laut, merah pala, dan krem dipersilakan.", colors: ["#123a63", "#b8282b", "#f3ead8", "#c99a42"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-09T09:00:00+09:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Jafar Marsaoly", "Kel. Besar Hi. Hamid Taher"] },
  },
});
