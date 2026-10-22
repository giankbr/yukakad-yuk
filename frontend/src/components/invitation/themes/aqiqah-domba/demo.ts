import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rayyan", groom: "",
    brideFull: "Muhammad Rayyan Al-Fatih",
    brideParents: "Putra pertama dari Bapak Fajar Nugroho & Ibu Annisa Putri Lestari",
    note: "Alhamdulillah, amanah kecil yang kami nanti telah hadir. Mohon doakan ia tumbuh menjadi anak yang saleh.",
  },
  eventLabel: "Aqiqah",
  date: "2027-03-14T09:00:00+07:00",
  place: "Kediaman Bapak Fajar Nugroho",
  address: "Jl. Sukaluyu No. 12, Cibeunying Kaler, Kota Bandung",
  story: { title: "", body: "" },
  stories: [
    { title: "Kabar gembira", date: "Juli 2026", body: "Hasil pemeriksaan pertama membuat kami sujud syukur bersama di ruang tunggu klinik." },
    { title: "Ahlan wa sahlan, Rayyan", date: "7 Mar 2027", body: "Lahir pukul 05.20 WIB, ba'da Subuh, dengan berat 3,4 kg dan panjang 50 cm." },
  ],
  events: [
    { name: "Tasyakuran Aqiqah", date: "2027-03-14T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Kediaman Bapak Fajar Nugroho", address: "Jl. Sukaluyu No. 12, Cibeunying Kaler, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7209 8812 34", account_name: "Annisa Putri Lestari" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0813 2244 6688", account_name: "Fajar Nugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Sukaluyu No. 12, Cibeunying Kaler, Kota Bandung 40123" },
  ],
  guestName: "Bapak Haris & Keluarga",
  guestTable: "",
  extras: {
    child: {
      name: "Muhammad Rayyan Al-Fatih",
      nickname: "Rayyan",
      birthDate: "2027-03-07T05:20:00+07:00",
      meaning: "Rayyan adalah nama pintu surga bagi orang-orang yang berpuasa, dan Al-Fatih berarti sang pembuka. Semoga ia tumbuh menjadi pribadi yang teduh, gemar beribadah, dan membuka banyak pintu kebaikan.",
      parents: "Putra pertama dari Bapak Fajar Nugroho & Ibu Annisa Putri Lestari",
    },
    quote: { text: "Setiap anak tergadai dengan aqiqahnya, disembelihkan (kambing) untuknya pada hari ketujuh, dicukur rambutnya, dan diberi nama.", source: "HR. Abu Dawud" },
    rundown: { items: [
      { time: "09.00", title: "Pembukaan & tilawah Al-Qur'an" },
      { time: "09.20", title: "Cukur rambut & doa untuk Rayyan" },
      { time: "10.00", title: "Tausiyah singkat" },
      { time: "10.30", title: "Ramah tamah & santap siang", note: "Hidangan aqiqah" },
    ] },
    dressCode: { note: "Busana muslim bernuansa pastel: hijau daun, krem, atau biru langit.", colors: ["#9fcf8c", "#f6efe2", "#cfe6f5", "#f6d3e0"] },
    rsvpDietary: {},
    family: { names: ["Kakek & Nenek dari Garut", "Kakek & Nenek dari Cirebon", "Keluarga besar Bani Nugroho"] },
    faq: { items: [
      { q: "Bolehkah menjenguk dan menggendong bayi?", a: "Boleh, mohon mencuci tangan terlebih dahulu dan tidak sedang sakit ya." },
      { q: "Apakah tersedia parkir?", a: "Parkir mobil tersedia di halaman masjid kompleks, ± 50 m dari rumah." },
    ] },
  },
});
