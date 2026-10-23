import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Fikri",
    brideFull: "Andi Ayu Mahdiyah, S.Ked.", groomFull: "Muhammad Fikri Daeng Nai, S.H.",
    brideParents: "Putri bungsu dari\nBapak H. Andi Muh. Yusran & Ibu Hj. Andi Rosdiana", groomParents: "Putra kedua dari\nBapak Drs. Abd. Rahman Daeng Sila & Ibu Hj. Nurhayati",
    note: "Seperti baju bodo yang ringan namun tegas warnanya, semoga rumah tangga kami lapang, terang, dan selalu dalam lindungan Allah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T09:00:00+08:00",
  place: "Masjid Amirul Mukminin",
  address: "Jl. Penghibur, Losari, Kec. Ujung Pandang, Kota Makassar",
  stories: [
    { date: "2021", title: "Koas di Wahidin", body: "Ayu sedang koas di RS Wahidin, Fikri mengantar neneknya kontrol. Obrolan singkat di lorong berlanjut sampai kantin." },
    { date: "2025", title: "Senja di Losari", body: "Setiap Jumat sore kami berjalan di anjungan Losari, menunggu matahari tenggelam sambil makan pisang epe." },
    { date: "2026", title: "Mammanu'-manu'", body: "Keluarga Fikri datang menjajaki dengan santun. Beberapa bulan kemudian, uang panai' disepakati dalam akkiyo' bicara." },
  ],
  events: [
    { name: "Mappacci", date: "2027-08-13T19:30:00+08:00", time: "19.30 – 21.30 WITA", venue: "Kediaman Mempelai Wanita", address: "Jl. Hertasning Baru No. 32, Rappocini, Kota Makassar" },
    { name: "Akad Nikah", date: "2027-08-14T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Amirul Mukminin", address: "Jl. Penghibur, Losari, Kec. Ujung Pandang, Kota Makassar" },
    { name: "Resepsi", date: "2027-08-14T19:00:00+08:00", time: "19.00 – 22.00 WITA", venue: "Balai Sidang Somba Opu", address: "Jl. Penghibur No. 21, Losari, Kec. Ujung Pandang, Kota Makassar" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r84.webp", "/themes/img/r105.webp", "/themes/img/r83.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7204 1189 3360", account_name: "Andi Ayu Mahdiyah" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0170 0109 4423 506", account_name: "Muhammad Fikri" },
    { id: "demo-kado", type: "address", address: "Jl. Hertasning Baru No. 32, Rappocini, Kota Makassar 90222", account_name: "Keluarga H. Andi Muh. Yusran" },
  ],
  guestName: "Bapak H. Abdul Hakim Daeng Tutu & Keluarga",
  guestTable: "Meja Losari 7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.00", title: "Penyambutan tamu", note: "Diiringi gendang dan pui'-pui'" },
      { time: "19.30", title: "Kedua mempelai memasuki pelaminan" },
      { time: "20.00", title: "Ramah tamah & makan malam", note: "Coto, konro, dan barongko" },
      { time: "21.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Baju bodo, jas tutup, atau busana muslim cerah. Jingga, hijau, dan emas dipersilakan.", colors: ["#ec5418", "#159a6a", "#c99a3f", "#12383d"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Andi Muh. Yusran", "Kel. Besar Drs. Abd. Rahman Daeng Sila"] },
  },
});
