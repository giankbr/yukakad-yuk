import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsabila", groom: "Arkan",
    brideFull: "Salsabila Nur Aini, S.Farm.", groomFull: "Arkan Fathurrahman, S.Kom.",
    brideParents: "Putri pertama dari\nBapak Ir. Dadang Kurniawan & Ibu Euis Rohmawati", groomParents: "Putra kedua dari\nBapak H. Ahmad Zaenudin & Ibu Hj. Siti Maryam",
    note: "Semoga Allah menghimpun kami dalam kebaikan, di dunia hingga ke surga-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T08:00:00+07:00",
  place: "Hotel Salak The Heritage",
  address: "Jl. Ir. H. Juanda No. 8, Paledang, Bogor Tengah, Kota Bogor",
  stories: [
    { date: "2023", title: "Kajian Ahad Pagi", body: "Kami sama-sama menjadi panitia kajian remaja masjid, tanpa banyak bicara satu sama lain." },
    { date: "2026", title: "Ta'aruf", body: "Melalui perantara guru ngaji, kami bertukar biodata dan bertemu didampingi keluarga." },
    { date: "2027", title: "Khitbah", body: "Dengan restu kedua orang tua, Arkan mengkhitbah Salsabila. Bismillah, kami melangkah bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Bogor Timur, Kota Bogor" },
    { name: "Walimah", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Hotel Salak The Heritage", address: "Jl. Ir. H. Juanda No. 8, Paledang, Bogor Tengah, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 4459 88", account_name: "Salsabila Nur Aini" },
    { id: "demo-kado", type: "address", address: "Perumahan Bogor Nirwana Residence Blok K3 No. 17, Mulyaharja, Bogor Selatan 16135" },
  ],
  guestName: "Ibu Hj. Nurlela & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Pembukaan & tilawah", note: "Qari' dari Pesantren Darul Qur'an" },
      { time: "11.20", title: "Tausiyah pernikahan", note: "Ustadz H. Mukhlis Hanafi" },
      { time: "11.50", title: "Ramah tamah" },
      { time: "13.00", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Nuansa tosca, putih, dan krem.", colors: ["#1f9488", "#9fe0d6", "#ffffff", "#e9dcc0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ir. Dadang Kurniawan", "Kel. Besar H. Ahmad Zaenudin"] },
    faq: { items: [
      { q: "Apakah area tamu dipisah?", a: "Ya, tamu pria dan wanita menempati area yang terpisah dengan pintu masuk masing-masing." },
      { q: "Apakah ada musala?", a: "Ada, musala tersedia di lantai dasar hotel untuk salat Zuhur." },
    ] },
  },
});
