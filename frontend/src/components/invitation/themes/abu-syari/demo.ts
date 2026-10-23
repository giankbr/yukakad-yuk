import { makeDemo } from "../demo-base";

// Syari tanpa foto: akad nikah di masjid dan walimah sederhana dengan tempat terpisah untuk tamu pria dan wanita.
export const demo = makeDemo({
  couple: {
    bride: "Hana", groom: "Rayyan",
    brideFull: "Hana Salsabila Azzahra", groomFull: "Rayyan Al-Farisi, Lc.",
    brideParents: "Putri pertama dari\nBapak Ahmad Zainuddin & Ibu Fatimah Az-Zahra", groomParents: "Putra kedua dari\nBapak Dr. Hasan Basri & Ibu Khadijah Nur",
    note: "Semoga Allah menghimpun kami dalam kebaikan, sederhana dalam rupa, lapang dalam syukur.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T08:00:00+07:00",
  place: "Graha Sakinah",
  address: "Jl. Raya Darmo No. 128, Wonokromo, Surabaya",
  stories: [
    { date: "2023", title: "Ta'aruf", body: "Dipertemukan melalui guru ngaji keluarga, kami saling mengenal dengan didampingi orang tua." },
    { date: "2026", title: "Khitbah", body: "Keluarga Rayyan datang meminang dengan niat baik, disambut doa dan restu kedua keluarga." },
    { date: "2027", title: "Akad Nikah", body: "Insyaallah kami menyempurnakan separuh agama, memohon doa agar menjadi keluarga sakinah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Nasional Al-Akbar", address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Graha Sakinah", address: "Jl. Raya Darmo No. 128, Wonokromo, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 2027 05", account_name: "Hana Salsabila Azzahra" },
    { id: "demo-kado", type: "address", address: "Jl. Ketintang Baru VII No. 14, Gayungan, Surabaya 60231" },
  ],
  guestName: "Ibu Hj. Maryam & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Pembukaan & tilawah" },
      { time: "11.20", title: "Tausiyah pernikahan", note: "Ustadz Abdullah Faqih" },
      { time: "12.00", title: "Ramah tamah", note: "Area tamu pria dan wanita terpisah" },
    ] },
    dressCode: { note: "Busana muslim sopan dalam nuansa abu-abu, putih, dan perak.", colors: ["#e7e8ea", "#b9bdc4", "#6f747c", "#ffffff"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ahmad Zainuddin", "Kel. Besar Dr. Hasan Basri"] },
  },
});
