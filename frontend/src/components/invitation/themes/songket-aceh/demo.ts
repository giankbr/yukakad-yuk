import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Humaira", groom: "Haikal",
    brideFull: "Cut Syarifah Humaira, S.Ked.", groomFull: "Teuku Haikal Mahmud, S.T.",
    brideParents: "Putri kedua dari\nBapak Teuku Ismail Hasan & Ibu Cut Nurhayati", groomParents: "Putra sulung dari\nBapak H. Mahmud Daud & Ibu Hj. Zuraida",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Seperti benang emas yang ditenun sehelai demi sehelai, semoga ikatan kami kuat, indah, dan diberkahi Allah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-23T08:00:00+07:00",
  place: "Anjong Mon Mata",
  address: "Jl. Sultan Alaidin Mahmudsyah, Peuniti, Baiturrahman, Banda Aceh",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2020", title: "Bertemu di Peunayong", body: "Satu meja di warung kopi yang penuh saat hujan sore. Obrolan tentang buku berlanjut sampai azan magrib." },
    { date: "2024", title: "Ba Ranub", body: "Keluarga Haikal datang membawa sirih (ranub) dalam batee ranub, tanda niat baik untuk meminang." },
    { date: "2027", title: "Hari yang Ditetapkan", body: "Dengan restu kedua keluarga, kami melangkah ke akad nikah dan walimah di Banda Aceh." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-23T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Baiturrahman", address: "Jl. Moh. Jam, Kampung Baru, Baiturrahman, Banda Aceh" },
    { name: "Peusijuek & Walimah", date: "2027-05-23T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Anjong Mon Mata", address: "Jl. Sultan Alaidin Mahmudsyah, Peuniti, Baiturrahman, Banda Aceh" },
  ],
  gallery: ["/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a122.webp", "/themes/img/a111.webp"],
  gifts: [
    { id: "demo-bas", type: "bank", bank_name: "Bank Aceh Syariah", account_number: "010 02 23 456789", account_name: "Cut Syarifah Humaira" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Teuku Haikal Mahmud" },
    { id: "demo-kado", type: "address", address: "Jl. Tgk. Chik Ditiro No. 21, Peuniti, Baiturrahman, Banda Aceh 23116" },
  ],
  guestName: "Bapak Teuku Zulkarnain & Keluarga",
  guestTable: "Meja Seulanga 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Intat linto baro", note: "Rombongan mempelai pria diantar dengan rapai" },
      { time: "11.30", title: "Peusijuek", note: "Tepung tawar oleh para tetua adat" },
      { time: "12.00", title: "Jamuan walimah", note: "Kuah beulangong & hidangan khas Aceh" },
    ] },
    dressCode: { note: "Busana muslim rapi. Merah, hitam, dan emas dipersilakan.", colors: ["#7a1517", "#191112", "#c4933a", "#f3e6cc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Teuku Ismail Hasan", "Kel. Besar H. Mahmud Daud", "Keluarga Besar Gampong Lambhuk"] },
  },
});
