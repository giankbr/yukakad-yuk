import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Firah", groom: "Ilham",
    brideFull: "Andi Nurul Magfirah, S.Psi.", groomFull: "Muhammad Ilham Daeng Rapi, S.E.",
    brideParents: "Putri bungsu dari\nBapak H. Andi Baso Mappaewa & Ibu Hj. Andi Rosmiati", groomParents: "Putra sulung dari\nBapak Drs. H. Syamsuddin Daeng Ngalle & Ibu Hj. Nurhayati Daeng Kanang",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Kualleangi tallanga na toalia — lebih baik tenggelam daripada kembali sebelum sampai. Kami berlayar bersama, sampai ke tujuan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-12-04T09:00:00+08:00",
  place: "Masjid Al-Markaz Al-Islami",
  address: "Jl. Masjid Raya No. 57, Bontoala, Kota Makassar, Sulawesi Selatan",
  stories: [
    { date: "2020", title: "Senja di Losari", body: "Kami berkenalan di anjungan Pantai Losari, menunggu matahari tenggelam sambil berbagi pisang epe." },
    { date: "2025", title: "Assuro", body: "Keluarga Ilham datang melamar. Kedua keluarga bermusyawarah dan menetapkan hari baik." },
    { date: "2027", title: "Akad Nikah", body: "Dengan memohon rida Allah, kami memulai pelayaran bersama, berbekal doa kedua orang tua." },
  ],
  events: [
    { name: "Mappacci", date: "2027-12-03T19:30:00+08:00", time: "19.30 – 21.30 WITA", venue: "Kediaman Mempelai Wanita", address: "Jl. Somba Opu No. 88, Losari, Ujung Pandang, Kota Makassar" },
    { name: "Akad Nikah", date: "2027-12-04T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Al-Markaz Al-Islami", address: "Jl. Masjid Raya No. 57, Bontoala, Kota Makassar" },
    { name: "Resepsi", date: "2027-12-04T19:00:00+08:00", time: "19.00 – 22.00 WITA", venue: "Gedung Pertemuan Anjungan Losari", address: "Jl. Penghibur No. 12, Losari, Ujung Pandang, Kota Makassar" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r2.webp", "/themes/img/r109.webp", "/themes/img/r0.webp", "/themes/img/r104.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7180 2240 63", account_name: "Andi Nurul Magfirah" },
    { id: "demo-bsulselbar", type: "bank", bank_name: "Bank Sulselbar", account_number: "160 002 000 448 21", account_name: "Muhammad Ilham Daeng Rapi" },
  ],
  guestName: "Bapak H. Abdul Rahman Daeng Sila & Keluarga",
  guestTable: "Meja Losari 6",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "19.00", title: "Penyambutan tamu", note: "Diiringi gandrang dan pui'-pui'" },
      { time: "19.30", title: "Doa & sambutan keluarga" },
      { time: "20.00", title: "Ramah tamah", note: "Coto, konro, dan kue-kue Makassar" },
      { time: "21.00", title: "Foto bersama" },
    ] },
    dressCode: { note: "Baju bodo atau busana muslim resmi; lipa' sabbe untuk bapak-bapak. Merah marun, emas, dan ungu senja dipersilakan.", colors: ["#3b2448", "#b0202c", "#d29a3a", "#f4b88a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-12-04T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Andi Baso Mappaewa", "Kel. Besar Drs. H. Syamsuddin Daeng Ngalle"] },
  },
});
