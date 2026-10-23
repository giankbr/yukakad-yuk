import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nayla", groom: "Faris",
    brideFull: "Nayla Khairunnisa Azzahra, S.Farm.", groomFull: "Muhammad Faris Al Ghifari, S.H.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Syarif & Ibu Hj. Siti Mardiyah", groomParents: "Putra pertama dari\nBapak Drs. Taufik Hidayat & Ibu Rahmawati",
    note: "Semoga Allah menghimpun kami dalam kebaikan, menjadikan rumah tangga kami sakinah, mawaddah, wa rahmah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-25T08:00:00+07:00",
  place: "Grha Sabha Pramana",
  address: "Jl. Pancasila, Bulaksumur, Kec. Depok, Kabupaten Sleman, Daerah Istimewa Yogyakarta",
  stories: [
    { date: "2021", title: "Kajian Ahad pagi", body: "Kami sama-sama menjadi panitia kajian remaja masjid. Tidak banyak bicara, hanya saling menitipkan doa dalam diam." },
    { date: "2025", title: "Ta'aruf", body: "Lewat perantara guru ngaji, Faris memberanikan diri bertukar biodata. Istikharah kami berujung pada keyakinan yang sama." },
    { date: "2026", title: "Khitbah", body: "Keluarga Faris datang ke Sleman dengan membawa niat baik. Bismillah, kami memulai persiapan menuju akad." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-25T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jogokariyan", address: "Jl. Jogokaryan No. 36, Mantrijeron, Kota Yogyakarta" },
    { name: "Walimatul 'Ursy", date: "2027-09-25T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Grha Sabha Pramana", address: "Jl. Pancasila, Bulaksumur, Kec. Depok, Kabupaten Sleman" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 3344 55", account_name: "Nayla Khairunnisa Azzahra" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri Syariah", account_number: "1370 0099 1234 5", account_name: "Muhammad Faris Al Ghifari" },
    { id: "demo-kado", type: "address", address: "Jl. Kaliurang Km 7 No. 14, Sinduharjo, Ngaglik, Sleman 55581" },
  ],
  guestName: "Ibu Hj. Fatimah Az-Zahra & Keluarga",
  guestTable: "Meja Mawar 2",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu" },
      { time: "11.20", title: "Tilawah & tausiyah singkat" },
      { time: "11.45", title: "Doa untuk kedua mempelai" },
      { time: "12.00", title: "Ramah tamah & foto bersama", note: "Area tamu putra dan putri dipisah" },
    ] },
    dressCode: { note: "Busana muslim yang sopan. Nuansa peach, krem, atau koral lembut.", colors: ["#f5b394", "#fbe8d8", "#e98068", "#a6b597"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarif (Sleman)", "Kel. Besar Drs. Taufik Hidayat (Klaten)"] },
  },
});
