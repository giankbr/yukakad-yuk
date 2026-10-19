import { makeDemo } from "../demo-base";

// Syari theme: no photos at all (the theme ignores portraits and gallery images).
export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Fikri",
    note: "Menyempurnakan separuh agama dengan niat ibadah dan langkah yang sederhana.",
    brideFull: "Aisyah Humaira Salsabila", groomFull: "Fikri Abdurrahman, S.Kom.",
    brideParents: "Putri dari Bapak Ust. Hasan Basri & Ibu Siti Khadijah",
    groomParents: "Putra dari Bapak H. Abdul Malik & Ibu Hj. Fatmawati",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-20T09:00:00+07:00",
  place: "Masjid Al-Ikhlas",
  address: "Jl. Cendana No. 12, Sukajadi, Bandung",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { title: "Ta'aruf", date: "Rajab 1447 H", body: "Bertukar biodata melalui perantara keluarga dan guru kami." },
    { title: "Nadzor & Khitbah", date: "Syawal 1447 H", body: "Pertemuan keluarga yang hangat, diakhiri dengan lamaran yang sederhana." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-20T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Al-Ikhlas", address: "Jl. Cendana No. 12, Sukajadi, Bandung" },
    { name: "Walimah", date: "2027-06-20T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Kediaman Mempelai Wanita", address: "Jl. Cendana No. 20, Sukajadi, Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7012 8899 0011", account_name: "Aisyah Humaira Salsabila" },
    { id: "demo-kado", type: "address", address: "Jl. Cendana No. 20, Sukajadi, Bandung 40162" },
  ],
  guestName: "Ibu Hj. Nurul Hidayah",
  guestTable: "",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "09.00", title: "Pembukaan & tilawah" },
      { time: "09.20", title: "Ijab kabul" },
      { time: "09.45", title: "Nasihat pernikahan" },
      { time: "11.00", title: "Walimah", note: "Area tamu pria dan wanita terpisah" },
    ] },
    dressCode: { note: "Busana muslim/muslimah yang longgar dan sopan, warna lembut.", colors: ["#c9d9cf", "#efd3cc", "#dcd5ea", "#f4ead8"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ust. Hasan Basri", "Kel. Besar H. Abdul Malik", "Keluarga Pondok Tahfidz Al-Ikhlas"] },
    faq: { items: [
      { q: "Apakah tempat tamu dipisah?", a: "Ya, area tamu pria dan wanita dipisah dengan hijab untuk menjaga kenyamanan." },
      { q: "Bolehkah mengambil foto?", a: "Mohon tidak memotret atau mengunggah foto mempelai ke media sosial." },
    ] },
  },
});
