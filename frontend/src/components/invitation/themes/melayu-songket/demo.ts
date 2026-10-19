import { makeDemo } from "../demo-base";

const base = makeDemo();

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Fadhil",
    brideFull: "Nur Aisyah Zahra, S.Pd.", groomFull: "Tengku Muhammad Fadhil, S.H.",
    brideParents: "Puteri bungsu dari\nBapak H. Wan Abdul Rahman & Ibu Hj. Siti Mariam",
    groomParents: "Putera kedua dari\nBapak Tengku Azhar Mahmud & Ibu Raja Nurhayati",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Sirih pulang ke gagang, pinang pulang ke tampuk.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T09:00:00+07:00",
  place: "Balai Adat Melayu Riau",
  address: "Jl. Diponegoro No. 39, Sukajadi, Pekanbaru",
  stories: [
    { date: "2018", title: "Bersua di Tepian Siak", body: "Berjumpa pertama kali saat festival Pacu Jalur, sama-sama menjadi relawan panitia dari kampus." },
    { date: "2022", title: "Merisik", body: "Keluarga Fadhil datang merisik dengan santun, menanyakan apakah Aisyah sudah ada yang punya." },
    { date: "2026", title: "Meminang & Antar Tanda", body: "Tepak sirih dan cincin tanda diantar; kedua keluarga bermufakat menetapkan hari baik bulan baik." },
  ],
  events: [
    { name: "Malam Berinai", date: "2027-06-18T19:30:00+07:00", time: "19.30 WIB – selesai", venue: "Kediaman Mempelai Wanita", address: "Jl. Hang Tuah No. 12, Sukajadi, Pekanbaru" },
    { name: "Akad Nikah", date: "2027-06-19T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Raya An-Nur", address: "Jl. Hang Tuah, Sumahilang, Pekanbaru" },
    { name: "Majlis Bersanding", date: "2027-06-19T11:30:00+07:00", time: "11.30 – 15.00 WIB", venue: "Balai Adat Melayu Riau", address: "Jl. Diponegoro No. 39, Sukajadi, Pekanbaru" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/r75.webp"],
  gifts: [
    { id: "demo-brk", type: "bank", bank_name: "BRK Syariah", account_number: "8101 2345 678", account_name: "Nur Aisyah Zahra" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0813 6512 3344", account_name: "Tengku Muhammad Fadhil" },
  ],
  guestName: "Bapak Datuk Zainal Arifin & Keluarga",
  extras: {
    ...base.extras,
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.30", title: "Berarak", note: "Rombongan pengantin diiringi kompang & silat" },
      { time: "12.00", title: "Bersanding di pelaminan" },
      { time: "12.15", title: "Tepuk tepung tawar", note: "Oleh para tetua & alim ulama" },
      { time: "12.45", title: "Makan beradab & ramah tamah" },
    ] },
    dressCode: { note: "Baju kurung, teluk belanga, atau busana Melayu bernuansa kuning-hijau.", colors: ["#0d4a35", "#2f7a55", "#e9b526", "#f6e7b0"] },
    family: { names: ["Kel. Besar H. Wan Abdul Rahman", "Kel. Besar Tengku Azhar Mahmud", "Lembaga Adat Kampung Bandar", "Keluarga Besar SMAN 1 Pekanbaru"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan terdekat.", items: [
      { name: "Hotel di Jl. Sudirman", detail: "± 2 km dari Balai Adat" },
      { name: "Bandara SSK II", detail: "± 20 menit berkendara ke lokasi" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh hadir di malam berinai?", a: "Malam berinai khusus keluarga dekat dan sahabat perempuan mempelai." },
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir di halaman Balai Adat Melayu Riau." },
    ] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-19T09:00:00+07:00" },
  },
});
