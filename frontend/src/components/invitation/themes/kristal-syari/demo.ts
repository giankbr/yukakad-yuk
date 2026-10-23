import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Fathan",
    brideFull: "Aisyah Hanun Salsabila, S.Farm.", groomFull: "Muhammad Fathan Ar-Rasyid, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Mahfud Ridwan & Ibu Hj. Nur Laili", groomParents: "Putra pertama dari\nBapak Drs. H. Imam Syafi'i & Ibu Hj. Umi Kulsum",
    note: "Seperti cahaya yang melewati kristal, semoga cinta kami terurai menjadi banyak warna kebaikan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T08:00:00+07:00",
  place: "Graha Sepuluh Nopember ITS",
  address: "Kampus ITS Sukolilo, Keputih, Kec. Sukolilo, Surabaya",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Satu Majelis Ilmu", body: "Kami mengikuti kajian pekanan yang sama di Masjid Manarul Ilmi ITS, duduk di sisi yang berbeda, mendengar nasihat yang sama." },
    { date: "2026", title: "Ta'aruf", body: "Melalui perantara guru ngaji, kami berkenalan dengan cara yang baik dan saling bertukar pandangan tentang rumah tangga yang ingin dibangun." },
    { date: "2027", title: "Akad Nikah", body: "Dengan rida Allah dan restu kedua keluarga, kami mengikat janji suci di Surabaya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Nasional Al-Akbar Surabaya", address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Graha Sepuluh Nopember ITS", address: "Kampus ITS Sukolilo, Keputih, Kec. Sukolilo, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7188 2041 55", account_name: "Aisyah Hanun Salsabila" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 3471 09", account_name: "Muhammad Fathan Ar-Rasyid" },
  ],
  guestName: "Ibu Hj. Siti Romlah & Keluarga",
  guestTable: "Meja Kristal 6",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu", note: "Area tamu putra dan putri terpisah" },
      { time: "11.30", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "11.45", title: "Tausiyah pernikahan" },
      { time: "12.15", title: "Doa & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim syar'i dengan warna lembut: putih gading, abu perak, atau pastel.", colors: ["#f7f4ee", "#c4cfd9", "#e9d6dc", "#d9e7dc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Mahfud Ridwan", "Kel. Besar Drs. H. Imam Syafi'i"] },
    faq: { items: [
      { q: "Apakah tempat duduk tamu dipisah?", a: "Ya, area tamu putra dan putri dipisah dengan pembatas, sesuai syariat." },
      { q: "Apakah tersedia tempat salat?", a: "Musala tersedia di sisi barat gedung, lengkap dengan tempat wudu." },
    ] },
  },
});
