import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Hanif",
    brideFull: "Zahra Nur Khalisah, S.Hum.", groomFull: "Hanif Abdurrahman Hakim, Lc.",
    brideParents: "Putri pertama dari\nBapak Dr. H. Ahmad Syarifuddin & Ibu Hj. Nurlaela", groomParents: "Putra ketiga dari\nBapak H. Abdul Hakim & Ibu Hj. Siti Fatimah",
    note: "Semoga Allah menghimpun kami dalam kebaikan, dan menjadikan rumah kami tempat ilmu dan dzikir bersemi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-13T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung",
  stories: [
    { date: "2021", title: "Di Ruang Naskah", body: "Kami bertemu di perpustakaan kampus, sama-sama meneliti naskah-naskah lama yang berhias iluminasi." },
    { date: "2025", title: "Ta'aruf", body: "Dengan perantaraan guru kami, kami saling mengenal dan memantapkan niat lewat istikharah." },
    { date: "2027", title: "Mitsaqan Ghaliza", body: "Dengan restu kedua orang tua, kami mengikat janji yang kokoh di hadapan Allah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-11-13T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-11-13T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Pusdai", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 3388 46", account_name: "Zahra Nur Khalisah" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "1460 0213 77", account_name: "Hanif Abdurrahman Hakim" },
  ],
  guestName: "Ustadz H. Muhammad Ridwan & Keluarga",
  guestTable: "Meja Mihrab 2",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Pembukaan & tilawah" },
      { time: "08.20", title: "Khutbah nikah & ijab kabul" },
      { time: "09.00", title: "Doa & nasihat pernikahan" },
    ] },
    dressCode: { note: "Busana muslim yang santun. Biru lapis, krem, dan emas dipersilakan.", colors: ["#1f3d8f", "#f5ecd6", "#c9a24a", "#c23b22"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Dr. H. Ahmad Syarifuddin", "Kel. Besar H. Abdul Hakim"] },
  },
});
