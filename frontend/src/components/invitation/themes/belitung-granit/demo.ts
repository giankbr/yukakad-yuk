import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aini", groom: "Hafiz",
    brideFull: "Nurul Aini Zulkarnain, S.Kep.", groomFull: "Muhammad Hafiz Ramadhan, S.Pi.",
    brideParents: "Putri sulung dari\nBapak H. Zulkarnain & Ibu Hj. Rosmawati",
    groomParents: "Putra ketiga dari\nBapak Syamsul Bahri & Ibu Hasnah",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti batu granit yang setia menjaga pantai, semoga cinta kami tenang, kokoh, dan sabar menghadapi pasang surut.",
  },
  eventLabel: "Walimatul 'Urus",
  date: "2027-09-11T10:00:00+07:00",
  place: "Gedung Serbaguna Tanjung Pendam",
  address: "Jl. Pantai Tanjung Pendam, Tanjung Pandan, Belitung",
  stories: [
    { date: "2020", title: "Relawan Bersih Pantai", body: "Kami bertemu saat memungut sampah plastik di Pantai Tanjung Tinggi. Hafiz membawa termos teh, Aini membawa kantong yang lebih banyak." },
    { date: "2025", title: "Berkenalan Keluarga", body: "Selepas Hafiz pulang dari tugas di Pulau Lengkuas, kami saling mengenal lebih dalam dengan restu kedua keluarga." },
    { date: "Juni 2027", title: "Merisik & Meminang", body: "Keluarga Hafiz datang membawa tepak sirih dan hantaran. Pinangan diterima dengan syukur dan senyum." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Ikhlas Tanjung Pandan", address: "Jl. Jend. Sudirman No. 18, Tanjung Pandan, Belitung" },
    { name: "Walimah", date: "2027-09-11T10:00:00+07:00", time: "10.00 – 14.00 WIB", venue: "Gedung Serbaguna Tanjung Pendam", address: "Jl. Pantai Tanjung Pendam, Tanjung Pandan, Belitung" },
  ],
  gallery: ["/themes/img/r15.webp", "/themes/img/r103.webp", "/themes/img/r9.webp", "/themes/img/r110.webp", "/themes/img/r107.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7193 0028 54", account_name: "Nurul Aini Zulkarnain" },
    { id: "demo-sumsel", type: "bank", bank_name: "Bank Sumsel Babel Syariah", account_number: "1820 6631 09", account_name: "Muhammad Hafiz Ramadhan" },
  ],
  guestName: "Bapak Datuk Ismail & Keluarga",
  guestTable: "Meja Lengkuas 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "10.00", title: "Arak-arakan pengantin", note: "Diiringi rebana dan hadrah" },
      { time: "10.30", title: "Bersanding & tepung tawar" },
      { time: "11.30", title: "Makan bedulang", note: "Gangan darat & kue rintak" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Baju kurung atau busana muslim bernuansa pantai: pasir putih, biru toska, dan abu granit.", colors: ["#f6f1e7", "#3fb8bf", "#1f7f9e", "#a8a39e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkarnain", "Kel. Besar Syamsul Bahri"] },
  },
});
