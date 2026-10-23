import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Annisa", groom: "Hafiz",
    brideFull: "Annisa Nurul Fitri, S.Psi.", groomFull: "Muhammad Hafiz Al-Ghifari, S.H.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Syarifuddin & Ibu Hj. Nur Aini", groomParents: "Putra pertama dari\nBapak Dr. Hasan Basri & Ibu Rahmah Fauziah",
    note: "Semoga Allah menjadikan pernikahan ini ladang pahala, seperti daun yang gugur dengan ikhlas untuk menyuburkan tanah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T08:00:00+07:00",
  place: "Aula Masjid Al-Hikmah",
  address: "Jl. Kaliurang Km 7,5, Sinduharjo, Ngaglik, Kabupaten Sleman, D.I. Yogyakarta",
  stories: [
    { date: "2021", title: "Ta'aruf", body: "Dikenalkan oleh ustadzah di kajian pekanan. Kami saling bertukar biodata dan bertemu didampingi keluarga." },
    { date: "2026", title: "Khitbah", body: "Keluarga Hafiz datang bersilaturahmi ke rumah dan menyampaikan niat baik. Alhamdulillah, diterima dengan hangat." },
    { date: "2027", title: "Akad", body: "Dengan izin Allah, kami menyempurnakan separuh agama di musim hujan pertama tahun ini." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Hikmah Sinduharjo", address: "Jl. Kaliurang Km 7,5, Sinduharjo, Ngaglik, Kabupaten Sleman" },
    { name: "Walimah", date: "2027-10-16T10:30:00+07:00", time: "10.30 – 13.00 WIB", venue: "Aula Masjid Al-Hikmah", address: "Jl. Kaliurang Km 7,5, Sinduharjo, Ngaglik, Kabupaten Sleman" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2233 69", account_name: "Annisa Nurul Fitri" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "5310 0088 47", account_name: "Muhammad Hafiz Al-Ghifari" },
    { id: "demo-kado", type: "address", address: "Perum Griya Kaliurang Asri Blok C-12, Sinduharjo, Ngaglik, Sleman 55581" },
  ],
  guestName: "Ustadzah Khadijah & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "10.30", title: "Kedatangan tamu", note: "Area putra & putri terpisah" },
      { time: "10.45", title: "Tilawah & tausiyah singkat" },
      { time: "11.30", title: "Doa bersama & ramah tamah" },
      { time: "12.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim/muslimah yang longgar dan sopan, nuansa hangat musim gugur.", colors: ["#d9a232", "#a4472a", "#f3e6c8", "#5a3a22"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Ahmad Syarifuddin", "Kel. Besar Bpk. Dr. Hasan Basri"] },
  },
});
