import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hana", groom: "Rayhan",
    brideFull: "Hana Salsabila Nuraini, S.Ds.", groomFull: "Muhammad Rayhan Alfarizi, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Syafi'i & Ibu Hj. Siti Rahmah", groomParents: "Putra pertama dari\nBapak Drs. Taufiq Hidayat & Ibu Nur Laila",
    note: "Dipertemukan di majelis ilmu, dikuatkan oleh doa kedua orang tua.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T08:00:00+07:00",
  place: "Gedung Wanitatama",
  address: "Jl. Laksda Adisucipto No. 88, Demangan, Gondokusuman, Kota Yogyakarta",
  story: { title: "", body: "" },
  stories: [
    { date: "Ramadan 2023", title: "Majelis Kamis Sore", body: "Kami sama-sama menjadi relawan kajian remaja di masjid kampus. Hanya bertegur sapa seperlunya, tanpa pernah berbincang panjang." },
    { date: "Agustus 2026", title: "Ta'aruf", body: "Lewat perantara guru ngaji kami, Ustazah Fatimah, kami bertukar biodata dan bertemu didampingi keluarga." },
    { date: "Desember 2026", title: "Khitbah", body: "Keluarga Rayhan datang meminang ke rumah di Kotagede. Alhamdulillah, lamaran diterima dengan penuh syukur." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jogokariyan", address: "Jl. Jogokaryan No. 36, Mantrijeron, Kota Yogyakarta" },
    { name: "Walimatul 'Ursy", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Gedung Wanitatama", address: "Jl. Laksda Adisucipto No. 88, Demangan, Gondokusuman, Kota Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7134 5520 81", account_name: "Hana Salsabila Nuraini" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "5310 0824 67", account_name: "Muhammad Rayhan Alfarizi" },
  ],
  guestName: "Ustaz H. Abdullah Faqih & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan", note: "Ustaz H. Salim Bahreisy" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
      { time: "12.00", title: "Ramah tamah & doa penutup" },
    ] },
    dressCode: { note: "Busana muslim/muslimah longgar bernuansa gading, krem, dan putih tulang.", colors: ["#f7f1e6", "#e6d9c4", "#c4a062", "#7d6e5d"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Kel. Besar Bani Syafi'i (Kotagede)", "Kel. Besar Bani Hidayat (Klaten)", "Keluarga Masjid Jogokariyan"] },
    faq: { items: [
      { q: "Apakah tempat duduk tamu dipisah?", a: "Ya, area tamu putra dan putri kami pisahkan dengan pembatas, dengan pintu masuk masing-masing." },
      { q: "Di mana bisa shalat Zuhur?", a: "Mushola tersedia di lantai dasar Gedung Wanitatama, lengkap dengan tempat wudhu." },
    ] },
  },
});
