import { makeDemo } from "../demo-base";

// Syari tanpa foto, gading dan emas: akad di masjid kampus, walimah sederhana di pendopo dengan area tamu terpisah.
export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Hamzah",
    brideFull: "Aisyah Nur Rahmah, S.Farm.", groomFull: "Hamzah Abdurrahman, M.Pd.",
    brideParents: "Putri ketiga dari\nBapak H. Muhammad Ridwan & Ibu Hj. Siti Maryam", groomParents: "Putra pertama dari\nBapak Abdul Karim & Ibu Ummu Salamah",
    note: "Semoga Allah menjadikan pernikahan ini ladang ibadah yang sederhana, bersih, dan penuh keberkahan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-10T08:00:00+07:00",
  place: "Pendopo Ndalem Gading",
  address: "Jl. Kaliurang Km. 9,5, Sardonoharjo, Ngaglik, Sleman, Yogyakarta",
  stories: [
    { date: "2024", title: "Ta'aruf", body: "Dikenalkan oleh ustadzah kajian pekanan, kami bertukar biodata dan saling mengenal dengan didampingi keluarga." },
    { date: "2026", title: "Khitbah", body: "Keluarga Hamzah datang meminang dengan niat baik, disambut doa dan restu kedua orang tua." },
    { date: "2027", title: "Mitsaqan Ghalizha", body: "Insyaallah kami mengikat perjanjian yang kokoh, memohon doa agar menjadi keluarga sakinah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-10T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Kampus UGM", address: "Jl. Tevesia, Karang Gayam, Caturtunggal, Depok, Sleman, Yogyakarta" },
    { name: "Walimatul 'Ursy", date: "2027-04-10T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Pendopo Ndalem Gading", address: "Jl. Kaliurang Km. 9,5, Sardonoharjo, Ngaglik, Sleman, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 4100 27", account_name: "Aisyah Nur Rahmah" },
    { id: "demo-kado", type: "address", address: "Jl. Palagan Tentara Pelajar No. 41, Ngaglik, Sleman, Yogyakarta 55581" },
  ],
  guestName: "Ibu Hj. Khadijah & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Pembukaan & tilawah" },
      { time: "11.20", title: "Tausiyah pernikahan", note: "Ustadz Fauzan Hamid" },
      { time: "12.00", title: "Ramah tamah", note: "Area tamu pria dan wanita terpisah" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Nuansa gading, krem, dan emas lembut.", colors: ["#f7f1e3", "#e6d8b8", "#b8914a", "#5a4e3c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Muhammad Ridwan", "Kel. Besar Abdul Karim"] },
  },
});
