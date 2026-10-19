import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Naura", groom: "",
    note: "Amanah kecil yang Allah titipkan untuk kami jaga dengan cinta.",
    brideFull: "Naura Kamila Azzahra",
    brideParents: "Putri pertama dari Bapak Arif Rahman & Ibu Laila Sari",
  },
  eventLabel: "Aqiqah",
  date: "2027-02-28T09:00:00+07:00",
  place: "Kediaman Bapak Arif Rahman",
  address: "Perum Griya Asri Blok C2 No. 7, Sleman, Yogyakarta",
  story: { title: "", body: "" },
  stories: [
    { title: "Kabar gembira", date: "Juni 2026", body: "Dua garis kecil yang membuat kami bersujud syukur bersama." },
    { title: "Selamat datang, Naura", date: "21 Feb 2027", body: "Lahir pukul 04.12 WIB dengan berat 3,2 kg dan panjang 49 cm, menjelang azan Subuh." },
  ],
  events: [
    { name: "Tasyakuran Aqiqah", date: "2027-02-28T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Kediaman Bapak Arif Rahman", address: "Perum Griya Asri Blok C2 No. 7, Sleman, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Laila Sari" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0857 1234 5678", account_name: "Arif Rahman" },
    { id: "demo-kado", type: "address", address: "Perum Griya Asri Blok C2 No. 7, Sleman, Yogyakarta 55581" },
  ],
  guestName: "Ibu Ratna & Keluarga",
  guestTable: "",
  extras: {
    child: {
      name: "Naura Kamila Azzahra",
      nickname: "Naura",
      birthDate: "2027-02-21T04:12:00+07:00",
      meaning: "Naura berarti bunga yang bercahaya, Kamila berarti sempurna, dan Azzahra berarti yang berseri. Semoga ia tumbuh menjadi pribadi yang berseri dan sempurna akhlaknya.",
      parents: "Putri pertama dari Bapak Arif Rahman & Ibu Laila Sari",
    },
    quote: { text: "Harta dan anak-anak adalah perhiasan kehidupan dunia, tetapi amal kebajikan yang terus-menerus adalah lebih baik pahalanya di sisi Tuhanmu.", source: "QS. Al-Kahf: 46" },
    rundown: { items: [
      { time: "09.00", title: "Pembukaan & tilawah" },
      { time: "09.20", title: "Cukur rambut & doa untuk Naura" },
      { time: "10.00", title: "Tausiyah singkat" },
      { time: "10.30", title: "Ramah tamah & santap siang" },
    ] },
    dressCode: { note: "Pakaian muslim bernuansa pastel.", colors: ["#f9c9d4", "#cdeee0", "#ffe3a3", "#cfdcff"] },
    rsvpDietary: {},
    family: { names: ["Kakek & Nenek dari Klaten", "Kakek & Nenek dari Magelang", "Keluarga besar Bani Rahman"] },
    faq: { items: [
      { q: "Bolehkah menjenguk dan menggendong bayi?", a: "Boleh, mohon mencuci tangan terlebih dahulu dan tidak sedang sakit ya." },
    ] },
  },
});
